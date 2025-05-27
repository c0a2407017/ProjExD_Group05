import pygame
import random


# 画面のサイズ
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
FPS = 60

# 色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 地面のY座標
GROUND_Y = 610

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.bottom = GROUND_Y
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 1
        self.jump_power = -20
        self.is_jumping = False
        self.world_x = 50

    def update(self):
        self.world_x += self.speed_x
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        if self.rect.bottom > GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.speed_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_power
            self.is_jumping = True

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = -5

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.kill()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("スーパーこうかとんブラザーズ")
    clock = pygame.time.Clock()

    # 背景画像
    bg_img = pygame.transform.rotozoom(pygame.image.load("ex5/fig/pg_bg.png").convert(), 0, 2.92)
    bg_width = bg_img.get_width()

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bird = Bird()
    all_sprites.add(bird)

    scroll_x = 0
    running = True
    game_over = False

    enemy_spawn_timer = 0
    enemy_spawn_interval = 90  # 約1.5秒

    font = pygame.font.Font(None, 80)  # フォント準備

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()

        if not game_over:
            keys = pygame.key.get_pressed()
            base_speed = 5
            speed = base_speed * 1.5 if keys[pygame.K_LSHIFT] else base_speed

            if keys[pygame.K_LEFT]:
                bird.speed_x = -speed
            elif keys[pygame.K_RIGHT]:
                bird.speed_x = speed
            else:
                bird.speed_x = 0

            all_sprites.update()
            enemies.update()

            enemy_spawn_timer += 1
            if enemy_spawn_timer >= enemy_spawn_interval:
                enemy_spawn_timer = 0
                enemy_x = scroll_x + SCREEN_WIDTH + 20
                enemy_y = GROUND_Y - 40
                enemy = Enemy(enemy_x, enemy_y)
                enemies.add(enemy)
                all_sprites.add(enemy)

            center_x = SCREEN_WIDTH // 2
            if bird.world_x > center_x:
                scroll_x = bird.world_x - center_x
            else:
                scroll_x = 0

            max_scroll = bg_width - SCREEN_WIDTH
            scroll_x = max(0, min(scroll_x, max_scroll))

            if bird.world_x > center_x:
                bird.rect.x = center_x
            else:
                bird.rect.x = bird.world_x

            if pygame.sprite.spritecollideany(bird, enemies):
                game_over = True
                game_over_time = pygame.time.get_ticks()  # ゲームオーバーになった時間

        screen.blit(bg_img, (-scroll_x, 0))
        all_sprites.draw(screen)

        if game_over:
            text = font.render("ゲームオーバー！", True, (255, 0, 0))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, rect)

            # ゲームオーバーから2秒経過したら終了
            if pygame.time.get_ticks() - game_over_time > 2000:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()