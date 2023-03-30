import pygame
import random
import os

WIDTH = 800
HEIGHT = 800

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

font_name = os.path.join("font.ttf")

#創建字體
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size) #傳入字體和大小
    text_surface = font.render(text, True, WHITE) #渲染 (文字 鋸齒 顏色)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

#復活次數
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 40*i #間隔30 像素
        img_rect.y = y
        surf.blit(img, img_rect) #畫出來

#生命值
def draw_health(surf, hp, x, y): #平面, 血量, 座標
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100 #生命條的長寬
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    if fill > BAR_LENGTH:
        fill = BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) #白色外框
    fill_ract = pygame.Rect(x, y, fill, BAR_HEIGHT) #綠色血條
    pygame.draw.rect(surf, GREEN, fill_ract)
    pygame.draw.rect(surf, WHITE, outline_rect, 2) #無填滿

#Boss生命值
def draw_boss_health(surf, hp, x, y): #平面, 血量, 座標
    if hp < 0:
        hp = 0
    BAR_LENGTH = 300 #生命條的長寬
    BAR_HEIGHT = 20
    fill = (hp/300)*BAR_LENGTH
    if fill > BAR_LENGTH:
        fill = BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) #白色外框
    fill_ract = pygame.Rect(x, y, fill, BAR_HEIGHT) #綠色血條
    pygame.draw.rect(surf, GREEN, fill_ract)
    pygame.draw.rect(surf, WHITE, outline_rect, 3) #無填滿

#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((50, 40))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speed = 6 #速度
        self.radius = 38 #半徑
        self.health = 100 #血量
        self.lives = 3 #復活次數
        self.hidden = False #飛船是否隱藏
        self.hidden_time = 0
        self.gun = 1
        self.gun_time = 0
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def update(self):
        now = pygame.time.get_ticks()
        #增加子彈
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hidden_time > 1000: #1000 毫秒 = 1秒
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10

        key_pressed = pygame.key.get_pressed() #回傳使用者按的按鍵
        if not(self.hidden):
            if key_pressed[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if key_pressed[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if key_pressed[pygame.K_UP]:
                self.rect.y -= self.speed
            if key_pressed[pygame.K_DOWN]:
                self.rect.y += self.speed

        if self.rect.right > WIDTH:  #讓飛船不會跑出界
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT and self.rect.bottom < 1300:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    #增加子彈
    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

    #飛船隱藏
    def hide(self):
        self.hidden = True
        self.hidden_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

#俗投
class Rock(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((30, 30))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2) #半徑
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -150)
        self.speedy = random.randrange(2, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)  #速度
            self.speedx = random.randrange(-3, 3)

#子彈
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((10, 30))
        #self.image.fill(YELLOW)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#掉寶
class Power(pygame.sprite.Sprite):
    def __init__(self, center, power_imgs):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'health'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)             #顏色
        self.rect = self.image.get_rect()      #定位
        self.rect.center = center
        self.speedy = 3                       #速度

    #操控
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

#護盾
class SHIELD(pygame.sprite.Sprite):
    def __init__(self, img, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT+500)
        self.radius = 42 #護盾大小
        self.time = 0 #持續時間
        self.now = False
        self.center = center

    def update(self):
        now = pygame.time.get_ticks()
        self.rect = self.center
        if self.now and now - self.time > 5000:
            self.kill()
        
    def power_on(self):
        self.now = True
        self.time = pygame.time.get_ticks()

#爆炸動畫
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, expl_anim):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.expl_anim = expl_anim
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 #爆炸的第一張動畫
        self.last_update = pygame.time.get_ticks() #最後一張圖片的時間
        self.frame_rate = 50 #經過?毫秒後更新圖片

    #操控
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate: 
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
            else:
                self.image = self.expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

#Boss動畫
class Boss_anime(pygame.sprite.Sprite): 
    def __init__(self, boss_anim):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_anim[0]
        self.boss_anim = boss_anim
        self.rect = self.image.get_rect()
        self.rect.center = (1500, 1500)
        self.radius = 100 #半徑
        self.health = 200 #血量
        self.frame = 0 #爆炸的第一張動畫
        self.last_update = pygame.time.get_ticks() #最後一張圖片的時間
        self.frame_rate = 80 #經過?毫秒後更新圖片

    #操控
    def update(self):
        self.rect.center = (410, 130)
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate: 
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.boss_anim):
                self.frame = 0
            else:
                self.image = self.boss_anim[self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

#Boss預告動畫
class BossComing(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT/2
        self.rect.centerx = WIDTH+500
        self.speedx = 10

    def update(self):
        self.rect.centerx -= self.speedx
        if self.rect.right < 0:
            self.kill()

#Boss本體
class Boss(pygame.sprite.Sprite):
    def __init__(self, body):
        pygame.sprite.Sprite.__init__(self)
        self.image = body
        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((700, 700))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (1500, 1500)
        self.radius = 350 #半徑
        self.health = 300 #血量
        #pygame.draw.circle(self.image, RED, (self.rect.right/2-25, self.rect.bottom/2-25), self.radius)

    def update(self):
        self.rect.x = 50
        self.rect.y = -500
