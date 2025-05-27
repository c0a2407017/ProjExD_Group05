import pygame 
import random
import sys
import time

# 画面のサイズ
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
FPS = 60

# 色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# ブロックの上端のy座標（背景画像に合わせて調整）
GROUND_Y = 610  

def check_bound(obj_rct:pygame.Rect,scroll_x) -> tuple[bool,bool]:
    yoko, tate = True, True
    if obj_rct.right  < scroll_x or SCREEN_WIDTH + scroll_x < obj_rct.left:
        yoko = False
    if obj_rct.top < 0 or SCREEN_HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate 

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ex5/fig/3.png")
        self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.bottom = GROUND_Y
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 1
        self.jump_power = -25      
        self.is_jumping = False
        self.world_x = 50

    def change_img(self,screen: pygame.Surface):
        self.image = pygame.transform.rotozoom(pygame.image.load(f"ex5/fig/8.png"), 0, 0.9)        
        screen.blit(self.image, self.rect)

    def update(self,screen):
        self.world_x += self.speed_x
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        if self.rect.bottom > GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.speed_y = 0
            self.is_jumping = False

        screen.blit(self.image,self.rect)

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_power
            self.is_jumping = True

class Enemy(pygame.sprite.Sprite):
    def __init__(self,scroll_x,bird_world_x):
        img = pygame.image.load("ex5/fig/0.png")
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(100 + scroll_x, SCREEN_WIDTH + scroll_x)
        self.world_x = random.randint(100 + scroll_x, 1100 + scroll_x)

        self.rect.y = -self.rect.height
        self.speed_y = 0
        self.gravity = 10
        self.speed = 0
        self.is_landed = False

        self.track_time = 1
        self.tracking = False
        self.bird_world_x = bird_world_x

    def update(self,scroll_x,bird_world_x):
        if not self.is_landed:
            self.speed_y += self.gravity
            self.rect.y = self.speed_y

            if self.rect.bottom >= GROUND_Y:
                self.rect.bottom = GROUND_Y
                self.is_landed = True
                self.speed_y = 0
                self.tracking = True
        else:
            if self.tracking and self.track_time > 0:
                if self.world_x > bird_world_x:
                    self.speed = -3
                elif self.world_x < bird_world_x:
                    self.speed = 3
                else:
                    self.speed = 0
                self.track_time -= 1
            else:
                self.tracking = False

            self.world_x += self.speed
            self.rect.move_ip(self.speed, 0)

        if check_bound(pygame.Rect(self.world_x, self.rect.y, self.rect.width, self.rect.height),scroll_x) != (True, True):
            self.kill() 

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("スーパーこうかとんブラザーズ")
    clock = pygame.time.Clock()

    bg_img = pygame.transform.rotozoom(pygame.image.load("ex5/fig/pg_bg.png").convert(), 0, 2.92)
    bg_width = bg_img.get_width()
    bg_height = bg_img.get_height()

    bird = Bird()
    emys = pygame.sprite.Group()

    scroll_x = 0
    tmr = 0

    while True:
        keys = pygame.key.get_pressed()
        speed = 10 if keys[pygame.K_LSHIFT] else 5  # ← Shiftでスピード2倍！

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump(

        # ←ここで左右キーの状態を見て速度を毎フレーム更新
        if keys[pygame.K_LEFT]:
            bird.speed_x = -speed
        elif keys[pygame.K_RIGHT]:
            bird.speed_x = speed
        else:
            bird.speed_x = 0

        center_x = SCREEN_WIDTH // 2
        if bird.world_x > center_x:
            scroll_x = bird.world_x - center_x
        else:
            scroll_x = 0

        max_scroll = bg_width - SCREEN_WIDTH
        if scroll_x > max_scroll:
            scroll_x = max_scroll
        if scroll_x < 0:
            scroll_x = 0

        if bird.world_x > center_x:
            bird.rect.x = center_x
        else:
            bird.rect.x = bird.world_x

        if tmr % 100 == 0:
            enemy = Enemy(scroll_x, bird.world_x)
            emys.add(enemy)

        for emy in pygame.sprite.spritecollide(bird, emys, True):
            screen.blit(bg_img, (-scroll_x, 0))
            bird.change_img(screen)
            emys.update(scroll_x,bird.world_x)
            for emy in emys:
                emy.rect.x = emy.world_x - scroll_x
                screen.blit(emy.image, emy.rect)
            pygame.display.update()
            time.sleep(2)
            return

        screen.blit(bg_img, (-scroll_x, 0))
        bird.update(screen)
        emys.update(scroll_x,bird.world_x)
        for emy in emys:
            emy.rect.x = emy.world_x - scroll_x
            screen.blit(emy.image, emy.rect)
        pygame.display.flip()

        tmr += 1
        clock.tick(50)

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
