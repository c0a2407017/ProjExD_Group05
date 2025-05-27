import pygame

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
GROUND_Y = 610  # 必要に応じて微調整してください

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.bottom = GROUND_Y  # ブロックの上に乗せる
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 1
        self.jump_power = -20
        self.is_jumping = False
        self.world_x = 50  # ワールド座標

    def update(self):
        # 左右移動
        self.world_x += self.speed_x
        # プレイヤーの画面上のx座標は後で調整

        # 重力
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        # 地面との衝突判定（ブロックの上）
        if self.rect.bottom > GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.speed_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_power
            self.is_jumping = True

    def grow(self):#キャラクターが大きくなる
        self.image = pygame.Surface([60, 100])
        self.image.fill(RED)
        old_rect = self.rect
        self.rect = self.image.get_rect()
        self.rect.centerx = old_rect.centerx
        self.rect.bottom = old_rect.bottom
        
class Mushroom(pygame.sprite.Sprite):#item
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x=-1
    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.kill()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("スーパーこうかとんブラザーズ")
    clock = pygame.time.Clock()

    # 背景画像のロード
    bg_img = pygame.transform.rotozoom(pygame.image.load("ex5/fig/pg_bg.png").convert(), 0, 2.92)
    bg_width = bg_img.get_width()
    bg_height = bg_img.get_height()

    all_sprites = pygame.sprite.Group()
    bird = Bird()
    all_sprites.add(bird)

    #itemを加える
    item_group = pygame.sprite.Group()
    item_group.add(
        Mushroom(800, GROUND_Y - 30),
    )
    
    scroll_x = 0  # 背景のスクロール量

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    bird.speed_x = -5
                if event.key == pygame.K_RIGHT:
                    bird.speed_x = 5
                if event.key == pygame.K_SPACE:
                    bird.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and bird.speed_x < 0:
                    bird.speed_x = 0
                if event.key == pygame.K_RIGHT and bird.speed_x > 0:
                    bird.speed_x = 0

        # ゲームループ
        all_sprites.update()
        item_group.update()#itemを呼び出す
        
        # プレイヤーが画面中央より右に行ったら背景をスクロール
        center_x = SCREEN_WIDTH // 2
        if bird.world_x > center_x:
            scroll_x = bird.world_x - center_x
        else:
            scroll_x = 0
        # 背景の範囲外に行かないように制限
        max_scroll = bg_width - SCREEN_WIDTH
        if scroll_x > max_scroll:
            scroll_x = max_scroll
        if scroll_x < 0:
            scroll_x = 0

        # プレイヤーの画面上のx座標を調整
        if bird.world_x > center_x:
            bird.rect.x = center_x
        else:
            bird.rect.x = bird.world_x

        # アイテムとの当たり判定＋関数を呼び出す
        if pygame.sprite.spritecollide(bird, item_group, dokill=True):#dokillはあたると消えるプログラむ
            bird.grow()
        # 描画
        screen.blit(bg_img, (-scroll_x, 0))
        
        # アイテムのスクロール対応描画
        for item in item_group:
            screen.blit(item.image, (item.rect.x - scroll_x, item.rect.y))

        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()