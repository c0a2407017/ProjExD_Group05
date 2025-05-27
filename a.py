import pygame
import sys

# 画面のサイズ
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
FPS = 60

# 色の定義（RGB）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# ブロックの上端のy座標（背景画像に合わせて調整）
GROUND_Y = 610  # 鳥が立つ地面の高さ

# プレイヤークラス（鳥）
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # プレイヤーの見た目（赤い四角）
        self.image = pygame.Surface([30, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 50  # 初期のx座標
        self.rect.bottom = GROUND_Y  # 地面の上に配置
        self.speed_x = 0  # 水平方向の速度
        self.speed_y = 0  # 垂直方向の速度（ジャンプ・落下）
        self.gravity = 1  # 重力加速度
        self.jump_power = -20  # ジャンプの初速
        self.is_jumping = False  # ジャンプ中フラグ
        self.world_x = 50  # ワールド座標（スクロール対応）

    def update(self):
        # 水平方向の移動
        self.world_x += self.speed_x
        
        # 重力による垂直速度の変化
        self.speed_y += self.gravity
        
        # 垂直方向の移動
        self.rect.y += self.speed_y

        # 地面に着いたらジャンプ状態解除
        if self.rect.bottom > GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.speed_y = 0
            self.is_jumping = False

    def jump(self):
        # ジャンプしていなければジャンプ開始
        if not self.is_jumping:
            self.speed_y = self.jump_power
            self.is_jumping = True

# 敵キャラクタークラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 敵の見た目（青い四角）
        self.image = pygame.Surface([40, 40])
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y  # 地面に配置

    def update(self):
        # 敵は今のところ動かさない（必要ならここに移動処理を追加）
        pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("スーパーこうかとんブラザーズ")
    clock = pygame.time.Clock()

    # 背景画像の読み込みとサイズ取得
    bg_img = pygame.transform.rotozoom(pygame.image.load("ex5/fig/pg_bg.png").convert(), 0, 2.92)
    bg_width = bg_img.get_width()

    # スプライトグループの作成
    all_sprites = pygame.sprite.Group()  # すべてのスプライト
    enemies = pygame.sprite.Group()     # 敵専用のグループ

    bird = Bird()  # プレイヤー作成
    all_sprites.add(bird)

    # 敵を複数配置（固定位置）
    enemy_positions = [(400, GROUND_Y), (700, GROUND_Y), (1000, GROUND_Y)]
    for pos in enemy_positions:
        enemy = Enemy(pos[0], pos[1])
        all_sprites.add(enemy)
        enemies.add(enemy)

    scroll_x = 0  # 背景のスクロール量
    running = True

    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # スペースキーでジャンプ
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # キーの押下状態を取得
        keys = pygame.key.get_pressed()

        # 左シフトを押していれば速度1.3倍にする
        base_speed = 5
        speed = base_speed * 1.3 if keys[pygame.K_LSHIFT] else base_speed

        # 左右キーで速度設定
        if keys[pygame.K_LEFT]:
            bird.speed_x = -speed
        elif keys[pygame.K_RIGHT]:
            bird.speed_x = speed
        else:
            bird.speed_x = 0

        # 全スプライトの状態更新
        all_sprites.update()

        # 衝突判定（鳥と敵がぶつかったらゲームオーバー）
        if pygame.sprite.spritecollideany(bird, enemies):
            # ゲームオーバー表示
            font = pygame.font.SysFont(None, 80)
            text = font.render("GAME OVER", True, (255, 0, 0))
            # 背景とスプライト描画
            screen.blit(bg_img, (-scroll_x, 0))
            all_sprites.draw(screen)
            # 中央にゲームオーバー文字表示
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(2000)  # 2秒停止
            running = False
            continue  # ループ終了へ

        # 画面中央より右に行ったら背景をスクロール
        center_x = SCREEN_WIDTH // 2
        if bird.world_x > center_x:
            scroll_x = bird.world_x - center_x
        else:
            scroll_x = 0

        # スクロール量を背景画像の範囲内に制限
        max_scroll = bg_width - SCREEN_WIDTH
        scroll_x = max(0, min(scroll_x, max_scroll))

        # 鳥の画面上のx座標調整（スクロール時は中央に固定）
        if bird.world_x > center_x:
            bird.rect.x = center_x
        else:
            bird.rect.x = bird.world_x

        # 背景画像描画（スクロール対応）
        screen.blit(bg_img, (-scroll_x, 0))
        # スプライト描画
        all_sprites.draw(screen)
        pygame.display.flip()

        # FPSに合わせて待機
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
