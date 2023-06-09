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
boss_coming = pygame.image.load(os.path.join("Game_img", "boss_coming.png")).convert()
#boss碰撞
boss_body = pygame.image.load(os.path.join("Game_img", "boss_body.png")).convert()
#boss受到攻擊
boss_harm = pygame.image.load(os.path.join("Game_img", "bossdamage.png")).convert()
#攻擊圖片
boss_attack = pygame.image.load(os.path.join("Game_img", "boss_attack.png")).convert()
#Boss子彈
boss_bullet = pygame.image.load(os.path.join("Game_img", "bossbullet.png")).convert()
 
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
    else:
        all_sprites.remove(r)

#攻擊
def Attack():
    a = BossAttack(boss.rect.bottom, boss_bullet)
    all_sprites.add(a)
    attacks.add(a)
         
#發射子彈
def shoot():
    if not(player.hidden):
        if player.gun == 1:
            bullet = Bullet(player.rect.centerx, player.rect.top, bullet_img)
            all_sprites.add(bullet)
            bullets.add(bullet)

        elif player.gun == 2:
            bullet1 = Bullet(player.rect.left, player.rect.centery, bullet_img)
            bullet2 = Bullet(player.rect.right, player.rect.centery, bullet_img)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)

        elif player.gun >= 3:
            bullet1 = Bullet(player.rect.centerx-30, player.rect.centery, bullet_img)
            bullet2 = Bullet(player.rect.centerx, player.rect.centery, bullet_img)
            bullet3 = Bullet(player.rect.centerx+30, player.rect.centery, bullet_img)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)

#初始畫面
def draw_init():
    draw_text(screen, "太空生存戰 !!!", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "上下左右鍵移動飛船, 空白艦發射子彈", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "攻擊隕石,獲得道具並擊敗Boss", 22, WIDTH/2, HEIGHT/2+25)
    draw_text(screen, "按任意鍵開始遊戲", 20, WIDTH/2, HEIGHT*3/4)
    #畫出隕石
    for i in range(len(rock_imgs)):
        draw_RockPic(screen, rock_imgs[i], 150*i, 10)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS) #60次/秒
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False

score = 0
running = True
Boss_show = True
Boss_coordinatex = 1500
Boss_coordinatey = 1500
last_update = 0
show_init = True

#遊戲運行
while running:
    if show_init:
        screen.blit(background, (0, 0))
        draw_init()
        show_init = False

        #群組
        all_sprites = pygame.sprite.Group()
        player = Player(player_img)
        boss_animes =  Boss_anime(boss_anim)
        boss = Boss(boss_body)
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        shields = pygame.sprite.Group()
        attacks = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        all_sprites.add(player)
        level = 1
        #石頭的群組
        for i in range(20):
            new_rock(level)
        #分數
        score = 0

    now = pygame.time.get_ticks()
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

    #Boss出現
    if score>=3000 and Boss_show:
        level = 2
        all_sprites.add(boss)
        coming = BossComing(boss_coming)
        all_sprites.add(coming) 
        all_sprites.add(boss_animes)
        Boss_coordinatex = 10
        Boss_coordinatey = 10
        last_update = pygame.time.get_ticks()
        player.hide()
        Boss_show = False

    #Boss攻擊
    if level == 2 and now - last_update > 2500 and boss.health>0:
        attack_anim = BossHarm(boss_attack, 500)
        all_sprites.add(attack_anim)
        Attack()
        last_update = pygame.time.get_ticks()

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

    #判斷護盾是否被Boss擊中
    hits = pygame.sprite.groupcollide(shields, attacks, True, True)
    for hit in hits:
        expl = Explosion(hit.rect.center, "lg", expl_anim)
        all_sprites.add(expl)

    #判斷Boss是否被擊中
    hits = pygame.sprite.spritecollide(boss, bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        boss.health -= 10
        bossharm = BossHarm(boss_harm, 200)
        all_sprites.add(bossharm)
        #如果血量歸零
        if boss.health <= 0:
            death_expl = Explosion(player.rect.center, "player", expl_anim)
            all_sprites.add(death_expl)
            all_sprites.remove(boss)
            boss.rect.center = (1500, 1500)
            all_sprites.remove(boss_animes)
            Boss_coordinatex = 1500
            Boss_coordinatey = 1500

    #判斷飛船被boss擊中
    hits = pygame.sprite.spritecollide(player, attacks, True)
    for hit in hits:
        player.health -= 50
        expl = Explosion(hit.rect.center, "lg", expl_anim)
        all_sprites.add(expl)
        #如果血量歸零
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, "player", expl_anim)
            all_sprites.add(death_expl)
            player.lives -= 1
            player.health = 100
            player.hide()

    if player.lives == 0 and not(death_expl.alive()): #當生命 = 0 和 die物件不存在時
        show_init = True

    if boss.health == 0 and not(death_expl.alive()): #當Boss被擊敗時
        show_init = True

    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, WIDTH/2, 10)
    draw_health(screen, player.health, player.rect.centerx-50, player.rect.centery + 40)
    draw_boss_health(screen, boss.health, Boss_coordinatex, Boss_coordinatey)
    draw_lives(screen, player.lives, lives_mini_img, WIDTH - 150, 20)
    pygame.display.update()

pygame.quit()
