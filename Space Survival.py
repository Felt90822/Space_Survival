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

#設定字體
font_name = os.path.join("font.ttf")

#新增石頭
def new_rock():
    img = random.choice(rock_imgs)
    r = Rock(img)
    all_sprites.add(r)
    rocks.add(r)
         
#發射子彈
def shoot():
    if not(player.hidden):
        bullet = Bullet(player.rect.centerx, player.rect.top, bullet_img)
        all_sprites.add(bullet)
        bullets.add(bullet)

#群組
all_sprites = pygame.sprite.Group()
player = Player(player_img)
bullets = pygame.sprite.Group()
all_sprites.add(player)

#石頭的群組
rocks = pygame.sprite.Group()
for i in range(7):
    new_rock()

score = 0
running = True
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

    #判斷石頭被擊中
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        score += hit.radius
        new_rock()

    #判斷石頭撞到飛船
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= (hit.radius-10)
        #如果血量歸零
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            player.hide()

    #畫面顯示 
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, lives_mini_img, WIDTH - 150, 20)
    pygame.display.update()

pygame.quit()
