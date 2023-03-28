import pygame
import os
from Object import *

FPS = 60
WIDTH = 800
HEIGHT = 800

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

#遊戲初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #長寬
pygame.display.set_caption("太空生存戰") #標題
clock = pygame.time.Clock()

#載入背景
background = pygame.image.load(os.path.join("Game_img", "background.png")).convert()
#載入石頭圖片
rock_imgs = []
for i in range(5):
    rock_imgs.append(pygame.image.load(os.path.join("Game_img", f"rock{i}.png")).convert())
#載入玩家圖片
player_img = pygame.image.load(os.path.join("Game_img", "player.png")).convert()
#載入子彈圖片
bullet_img = pygame.image.load(os.path.join("Game_img", "bullet.png")).convert()
#載入復活次數圖片
lives_img = pygame.image.load(os.path.join("Game_img", "lives.png")).convert()
lives_mini_img = pygame.transform.scale(lives_img, (30, 21))
lives_mini_img.set_colorkey(BLACK)
#載入護盾圖片
shield_img = pygame.image.load(os.path.join("Game_img", "shield_img.png")).convert()
#載入Boss預告
boss_coming = pygame.image.load(os.path.join("Game_img", "boss_attact.png")).convert()
 
#爆炸動畫
expl_anim = {}
expl_anim["lg"] = []
expl_anim["sm"] = []
expl_anim["player"] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("Game_img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim["lg"].append(pygame.transform.scale(expl_img, (90, 90)))
    expl_anim["sm"].append(pygame.transform.scale(expl_img, (50, 50)))

    player_expl_img = pygame.image.load(os.path.join("Game_img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim["player"].append(player_expl_img)

#寶物
power_imgs = {}
power_imgs["shield"] = pygame.image.load(os.path.join("Game_img", "shield.png")).convert()
power_imgs["gun"] = pygame.image.load(os.path.join("Game_img", "gun.png")).convert()
power_imgs["health"] = pygame.image.load(os.path.join("Game_img", "health.png")).convert()

#Boss動畫
boss_anim = []
for i in range(8):
    boss_img = pygame.image.load(os.path.join("Game_img", f"boss{i}.png")).convert()
    boss_img.set_colorkey(BLACK)
    boss_anim.append(boss_img)

#設定字體
font_name = os.path.join("font.ttf")

#新增石頭
def new_rock(level):
    img = random.choice(rock_imgs)
    r = Rock(img)
    if level == 1:
        all_sprites.add(r)
        rocks.add(r)
         
#發射子彈
def shoot():
    if not(player.hidden):
            if player.gun == 1:
                bullet = Bullet(player.rect.centerx, player.rect.top, bullet_img)
                all_sprites.add(bullet)
                bullets.add(bullet)

            elif player.gun >= 2:
                bullet1 = Bullet(player.rect.left, player.rect.centery, bullet_img)
                bullet2 = Bullet(player.rect.right, player.rect.centery, bullet_img)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
       
#群組
all_sprites = pygame.sprite.Group()
player = Player(player_img)
boss_animes =  Boss_anime(boss_anim)
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
shields = pygame.sprite.Group()
all_sprites.add(player)

level = 1
#石頭的群組
rocks = pygame.sprite.Group()
for i in range(7):
    new_rock(level)

score = 0
running = True
Boss_show = True

while running:
    clock.tick(FPS) #60次/秒

    #取得輸入
    for event in pygame.event.get(): #關閉視窗
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot() 

    #更新遊戲
    all_sprites.update()

    if score > 200 and Boss_show:
        level = 2
        coming = BossComing(boss_coming)
        all_sprites.add(coming) 
        all_sprites.add(boss_animes)
        #boss = Boss()
        #all_sprites.add(boss)
        Boss_show = False
    
    if score > 1000:
        all_sprites.remove(boss_animes)
    
    #判斷石頭被擊中
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        score += hit.radius
        expl = Explosion(hit.rect.center, "lg", expl_anim)
        all_sprites.add(expl)
        if random.random() > 0.9: #回傳0-1隨機數字
            power = Power(hit.rect.center, power_imgs)
            all_sprites.add(power)
            powers.add(power)
        new_rock(level)

    #判斷石頭撞到飛船
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock(level)
        player.health -= (hit.radius-10)
        expl = Explosion(hit.rect.center, "sm", expl_anim)
        all_sprites.add(expl)
        #如果血量歸零
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, "player", expl_anim)
            all_sprites.add(death_expl)
            player.lives -= 1
            player.health = 100
            player.hide()

    #判斷寶物是否擊中飛船
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == "shield":
            shield = SHIELD(shield_img, player.rect)
            shield.power_on()
            all_sprites.add(shield)
            shields.add(shield)
            
        elif hit.type == "gun":
            player.gunup()

        elif hit.type == "health":
            player.health += 20
            if player.health > 100:
                player.health = 100

    #判斷護盾是否被擊中
    hits = pygame.sprite.groupcollide(shields, rocks, True, True)
    for hit in hits:
        expl = Explosion(hit.rect.center, "lg", expl_anim)
        all_sprites.add(expl)
        new_rock(level)

    #判斷Boss是否被擊中
    hits = pygame.sprite.spritecollide(boss_animes, bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        draw_text(screen, "擊中!", 25, WIDTH/2, 400)
    
    #畫面顯示
    
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, WIDTH/2, 10)
    draw_health(screen, player.health, player.rect.centerx-50, player.rect.centery + 40)
    draw_lives(screen, player.lives, lives_mini_img, WIDTH - 150, 20)
    pygame.display.update()

pygame.quit()
