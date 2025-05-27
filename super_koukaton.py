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

# block_normalの位置リスト
BLOCK_NORMAL_POS = [(20, 4), (22, 4), (24, 4), (77, 4), (79, 4), (80, 8), (81, 8), (82, 8), (83, 8), (84, 8), (85, 8), (86, 8), (91,8), (92, 8), (93, 8), (94, 4), (100, 4), (101, 4), (118, 4), (121, 8), (122, 8), (123, 8), (128, 8), (129, 4), (130, 4), (131, 8), (168, 4), (169, 4), (171, 4), ]

# block_transparentの位置リスト
BLOCK_TRANSPARENT_POS = [(28, 1), (28, 2), (29, 1), (29, 2), (38, 1), (38, 2), (38, 3), (39, 1), (39, 2), (39, 3), (46, 1), (46, 2), (46, 3), (46, 4), (47, 1), (47, 2), (47, 3), (47, 4), (57, 1), (57, 2), (57, 3), (57, 4), (58, 1), (58, 2), (58, 3), (58, 4), (134, 1), (135, 1), (135, 2), (136, 1), (136, 2), (136, 3), (137, 1), (137, 2), (137, 3), (137, 4), (140, 1), (140, 2), (140, 3), (140, 4), (141, 1), (141, 2), (141, 3), (142, 1), (142, 2), (143, 1), (148, 1), (149, 1), (149, 2), (150, 1), (150, 2), (150, 3), (151, 1), (151, 2), (151, 3), (151, 4), (152, 1), (152, 2), (152, 3), (152, 4), (155, 1), (155, 2), (155, 3), (155, 4), (156, 1), (156, 2), (156, 3), (157, 1), (157, 2), (158, 1), (163, 1), (163, 2), (164, 1), (164, 2), (179, 1), (179, 2), (180, 1), (180, 2), (181, 1), (182, 1), (182, 2), (183, 1), (183, 2), (183, 3), (184, 1), (184, 2), (184, 3), (184, 4), (185, 1), (185, 2), (185, 3), (185, 4), (185, 5), (186, 1), (186, 2), (186, 3), (186, 4), (186, 5), (186, 6), (187, 1), (187, 2), (187, 3), (187, 4), (187, 5), (187, 6), (187, 7), (188, 1), (188, 2), (188, 3), (188, 4), (188, 5), (188, 6), (188, 7), (188, 8), (189, 1), (189, 2), (189, 3), (189, 4), (189, 5), (189, 6), (189, 7), (189, 8), (198, 1)]

# block_questionの位置リスト
BLOCK_QUESTION_POS = [(16, 4), (21, 4), (22, 8), (23, 4), (78, 4), (94, 8), (106, 4), (109, 4), (109, 8), (112, 4), (129, 8), (130, 8), (170, 4)]

MUSHROOM_POS = [(21, 4)]  # キノコが出現するブロックの位置

# 落とし穴の位置リスト
FALLING_PIT_POS = [(69, 70) , (86, 88), (153, 154)]

# ゴールの位置
GOAL_POS = (198, 1)  # ゴールの位置（x座標, y座標）

# ブロックの上端のy座標（背景画像に合わせて調整）
GROUND_Y = 610  # 必要に応じて微調整してください

class CustomGroup(pygame.sprite.Group):
    def call_method(self, method_name, *args, **kwargs):
        """
        グループ内のすべてのスプライトに対して指定されたメソッドを呼び出す。
        :param method_name: 呼び出すメソッドの名前（文字列）
        :param args: メソッドに渡す引数
        :param kwargs: メソッドに渡すキーワード引数
        """
        for sprite in self.sprites():
            method = getattr(sprite, method_name, None)  # メソッドを取得
            if callable(method):  # メソッドが存在し、呼び出し可能か確認
                method(*args, **kwargs)

class Player(pygame.sprite.Sprite):
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
        self.status = "normal"
        self.world_x = 50 # ワールド座標
        self.GROUND_Y = GROUND_Y  # 地面のy座標
        self.gaol_pos = (int(GOAL_POS[0] * 16 * 2.92), int(GROUND_Y - GOAL_POS[1] * 16 * 2.92))  # ゴールの位置
        self.gaol_speed_x = 1.3  # ゴールに到達したときの横移動速度
        self.diray = 0  # ディレイ（必要に応じて使用）


    def update_y(self):
        # ゴールの処理
        if self.gaol_pos[0] <= self.world_x < self.gaol_pos[0] + self.gaol_speed_x:
            self.reach_goal_y()
        # 重力
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        # 地面との衝突判定（ブロックの上）
        if self.rect.bottom > self.GROUND_Y:
            self.rect.bottom = self.GROUND_Y
            self.speed_y = 0
            self.is_jumping = False

        # 画面の外に出たら終了
        if self.rect.top > SCREEN_HEIGHT:
            #　ゲームオーバー処理
            self.kill()  # スプライトを削除
            print("ゲームオーバー")
            pygame.quit()
            exit()


    def update_x(self):
        # ゴールの処理
        if self.world_x >= self.gaol_pos[0]:
            self.speed_x = 0  # ゴールに到達したら横移動を停止
        if self.world_x >= self.gaol_pos[0] and self.rect.bottom >= self.gaol_pos[1]:
            self.reach_goal_x()

         # 左右移動
        self.world_x += self.speed_x
        self.rect.x = self.world_x  # ←ここで毎回world_xから計算

        # 落とし穴の処理
        nofalls = []
        for pit in FALLING_PIT_POS:
            pit_rect = (pit[0] * 16 * 2.92, (pit[1] + 1) * 16 * 2.92)
            if pit_rect[0] <= self.rect.right <= pit_rect[1]   :
                self.GROUND_Y += 400  # 落とし穴に落ちたら地面を下げる
                # if self.rect.bottom > GROUND_Y:
                #     if self.rect.left < pit_rect[0]:
                #         self.rect.left = pit_rect[0]
                #         self.world_x = self.rect.x  # ←world_xも修正
                #         self.speed_x = 0
                #     elif self.rect.right > pit_rect[1]:
                #         self.rect.right = pit_rect[1]
                #         self.world_x = self.rect.x  # ←world_xも修正
                #         self.speed_x = 0
            else:
                nofalls += [1]
        if len(nofalls) == len(FALLING_PIT_POS):
            self.GROUND_Y = GROUND_Y  # 落とし穴から出たら元の地面の位置に戻す

            

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_power
            self.is_jumping = True

    # ゴール到着のy座標処理
    def reach_goal_y(self):
        # ゴールに到達した場合の処理
        self.world_x = self.gaol_pos[0]
        self.rect.centerx = self.world_x  # ←world_xも修正
        if self.rect.bottom < self.gaol_pos[1]:
            self.speed_y = 0
            self.gravity = 1.5

    # ゴール到着のx座標処理
    def reach_goal_x(self):
        self.speed_x = self.gaol_speed_x  # ゴールに到達したら横移動速度を設定
        self.speed_y = 0
        if self.world_x >= int(204.2 * 16 * 2.92):
            self.status = "goal"  # ゴール状態に変更
            # 3秒待ってからゲーム終了
            if self.diray == 30 * 5:  # 3秒待つ
                # 3秒待ってからゲーム終了
                pygame.quit()
                exit()
            else:
                self.diray += 1


        

class Block_nomal(pygame.sprite.Sprite):
    def __init__(self, xy: tuple[int, int]):
        super().__init__()
        img = pygame.transform.rotozoom(pygame.image.load("fig/block_nomal.png").convert(), 0, 2.92)
        self.image = img
        self.image.set_colorkey(WHITE)  # 白色を透明にする
        self.rect = self.image.get_rect()
        self.rect.center = (xy[0] * 2 + 1)* 8 * 2.92,  GROUND_Y - (xy[1] * 2 - 1) * 8 * 2.92
        self.gravity = 1  # 重力の値
        self.speed_y = 0  # 縦方向の速度
        self.status = "normal"  # ブロックの状態（通常、壊れたなど）
        self.original_y = self.rect.y  # 元の位置を記録
    
    def update_y(self, player):
        # ブロックの更新処理（必要に応じて追加）
        if player is not None:
            if self.rect.colliderect(player.rect):
                # ここに当たり判定の処理を追加
                if player.speed_y < 0:
                    # プレイヤーが上からブロックに衝突した場合
                    player.rect.top = self.rect.bottom
                    player.world_y = player.rect.y  # ←world_yも修正
                    player.speed_y = 0  # ジャンプの速度をリセット
                    if player.status == "big":
                        # ビッグマリオの場合、ブロックを壊す
                        self.kill()
                        # ブロックを壊すアニメーションや効果音をここに追加することも可能
                    else:
                        # 小さいマリオの場合、ブロックを少し押し上げる
                        self.status = "active"  # ブロックの状態をアクティブにする
                        self.speed_y = -3  # 少し上に押し上げる
                if player.speed_y > 0 :
                    # プレイヤーが下からブロックに衝突した場合
                    player.rect.bottom = self.rect.top
                    player.world_y = player.rect.y  # ←world_yも修正
                    player.speed_y = 0
                    player.is_jumping = False  # ジャンプ状態をリセット


            if self.status == "active":
                # アクティブ状態のブロックの処理
                self.speed_y += self.gravity
                self.rect.y += self.speed_y
                # 元の位置に戻ったら停止
                if self.rect.y >= self.original_y:
                    self.rect.y = self.original_y
                    self.speed_y = 0
                    self.status = "normal"

    def update_x(self, player):
        # 横方向の更新処理（必要に応じて追加）
        if player is not None:
            if self.rect.colliderect(player.rect):
                # ここに当たり判定の処理を追加
                if player.speed_x > 0 and player.rect.left < self.rect.right:
                    # プレイヤーが右からブロックに衝突した場合
                    player.rect.right = self.rect.left
                    player.world_x = player.rect.x  # ←world_xも修正
                elif player.speed_x < 0 and player.rect.right > self.rect.left:
                    # プレイヤーが左からブロックに衝突した場合
                    player.rect.left = self.rect.right
                    player.world_x = player.rect.x  # ←world_xも修正
        

class Block_transparent(pygame.sprite.Sprite):
    def __init__(self, xy: tuple[int, int]):
        super().__init__()
        #透明な壁を作る
        #画像サイズを16x16にして、拡大している
        img = pygame.transform.rotozoom(pygame.image.load("fig/block_nomal.png").convert(), 0, 2.92)
        img.fill(WHITE)
        self.image = img
        self.image.set_colorkey(WHITE)  # 白色を透明にする
        self.rect = self.image.get_rect()
        self.rect.center = (xy[0] * 2 + 1)* 8 * 2.92,  GROUND_Y - (xy[1] * 2 - 1) * 8 * 2.92
    
    def update_y(self, player):
        # ブロックの更新処理（必要に応じて追加）
        if player is not None:
            if self.rect.colliderect(player.rect):
                # ここに当たり判定の処理を追加
                if player.speed_y < 0:
                    # プレイヤーが上からブロックに衝突した場合
                    player.rect.top = self.rect.bottom
                    player.world_y = player.rect.y  # ←world_yも修正
                    player.speed_y = 0  # ジャンプの速度をリセット
                if player.speed_y > 0 and player.rect.top < self.rect.bottom:
                    # プレイヤーが下からブロックに衝突した場合
                    player.rect.bottom = self.rect.top
                    player.world_y = player.rect.y  # ←world_yも修正
                    player.speed_y = 0
                    player.is_jumping = False  # ジャンプ状態をリセット

    def update_x(self, player):
        # 横方向の更新処理（必要に応じて追加）
        if player is not None:
            if self.rect.colliderect(player.rect):
                # ここに当たり判定の処理を追加
                if player.speed_x > 0 and player.rect.left < self.rect.right:
                    # プレイヤーが右からブロックに衝突した場合
                    player.rect.right = self.rect.left
                    player.world_x = player.rect.x  # ←world_xも修正
                elif player.speed_x < 0 and player.rect.right > self.rect.left:
                    # プレイヤーが左からブロックに衝突した場合
                    player.rect.left = self.rect.right
                    player.world_x = player.rect.x  # ←world_xも修正

class Block_question(pygame.sprite.Sprite):
    def __init__(self, xy: tuple[int, int], all_sprites: pygame.sprite.Group, MUSHROOM_POS: list, mushroom: pygame.sprite.Group):
        super().__init__()
        img = pygame.transform.rotozoom(pygame.image.load("fig/block_question.png").convert(), 0, 2.92)
        self.image = img
        self.image.set_colorkey(WHITE)  # 白色を透明にする
        self.rect = self.image.get_rect()
        self.rect.center = (xy[0] * 2 + 1)* 8 * 2.92,  GROUND_Y - (xy[1] * 2 - 1) * 8 * 2.92
        self.gravity = 1  # 重力の値
        self.speed_y = 0  # 縦方向の速度
        self.status = "normal"  # ブロックの状態（通常、壊れたなど）
        self.mushroom = mushroom  # キノコのクラス
        self.mushroom_pos = MUSHROOM_POS
        self.all_sprites = all_sprites
        self.original_y = self.rect.y  # 元の位置を記録
        self.xy = xy  # ブロックの位置を記録
    

    def update_y(self, player):
        # ブロックの更新処理（必要に応じて追加）
        if player is not None:
            if self.rect.colliderect(player.rect):
                # ここに当たり判定の処理を追加
                if player.speed_y < 0:
                    # プレイヤーが上からブロックに衝突した場合
                    player.rect.top = self.rect.bottom
                    player.world_y = player.rect.y  # ←world_yも修正
                    player.speed_y = 0  # ジャンプの速度をリセット
                    #　画像を切り替える
                    self.image = pygame.transform.rotozoom(pygame.image.load("fig/block_end.png").convert(), 0, 2.92)
                    #ブロックを少し押し上げる
                    if self.status == "normal":
                        self.status = "active"  # ブロックの状態をアクティブにする
                        self.speed_y = -3  # 少し上に押し上げる
                        if self.xy in self.mushroom_pos:
                            # キノコを出現させる
                            Mushroom1 = Mushroom(self.xy)  # キノコのインスタンスを作成
                            self.all_sprites.add(Mushroom1)  # 全スプライトグループに追加
                            self.mushroom.add(Mushroom1)  # キノコをグループに追加
                if player.speed_y > 0 :
                    # プレイヤーが下からブロックに衝突した場合
                    player.rect.bottom = self.rect.top
                    player.world_y = player.rect.y  # ←world_yも修正
                    player.speed_y = 0
                    player.is_jumping = False  # ジャンプ状態をリセット
                    


            if self.status == "active":
                # アクティブ状態のブロックの処理
                self.speed_y += self.gravity
                self.rect.y += self.speed_y
                # 元の位置に戻ったら停止
                if self.rect.y >= self.original_y:
                    self.rect.y = self.original_y
                    self.speed_y = 0
                    self.status = "end"  # 状態を終了に変更

    def update_x(self, player):
        # 横方向の更新処理（必要に応じて追加）
        if player is not None:
            if self.rect.colliderect(player.rect):
                # ここに当たり判定の処理を追加
                if player.speed_x > 0 and player.rect.left < self.rect.right:
                    # プレイヤーが右からブロックに衝突した場合
                    player.rect.right = self.rect.left
                    player.world_x = player.rect.x  # ←world_xも修正
                elif player.speed_x < 0 and player.rect.right > self.rect.left:
                    # プレイヤーが左からブロックに衝突した場合
                    player.rect.left = self.rect.right
                    player.world_x = player.rect.x  # ←world_xも修正


# キノコのクラス
class Mushroom(pygame.sprite.Sprite):
    def __init__(self, xy):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("fig/mushroom.png").convert(), 0, 2.92)
        self.image.set_colorkey(BLACK)  # 白色を透明にする
        self.rect = self.image.get_rect()
        self.xy = xy  # キノコの位置を記録
        self.rect.center = (xy[0] * 2 + 1)* 8 * 2.92,  GROUND_Y - (xy[1] * 2 - 1) * 8 * 2.92 
        self.speed_y = 0  # 上に移動する速度
        self.speed_x = 2.4  # 横方向の速度
        self.gravity =0.4  # 重力の値
        self.calculated_x = int((self.xy[0] * 2 + 1) * 8 * 2.92)
        self.calculated_y = GROUND_Y - ((self.xy[1] + 1)  * 2 - 1) * 8 * 2.92

    def update_y(self):
        
        if self.rect.centerx == self.calculated_x and self.rect.centery > self.calculated_y:
                #  キノコがブロックの上に来るまで上昇
                self.speed_y =  -1 # 上に移動する速度
                self.rect.y += self.speed_y
        else:
            # 重力
            self.speed_y += self.gravity
            self.rect.y += self.speed_y

        # 地面との衝突判定
        if self.rect.bottom > GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.speed_y = 0

        if self.rect.bottom < 0:  # 画面外に出たら削除
            self.kill()

    def update_x(self):
        if not (self.rect.centerx == self.calculated_x and self.rect.centery > self.calculated_y):
            self.rect.x += self.speed_x

    #  キノコの横方向の衝突判定
    def check_collision(self, player, blocks):
        if player.rect.colliderect(self.rect):
            print("キノコとプレイヤーが衝突しました")
            # ここにプレイヤーとの当たり判定の処理を追加
            if player.status == "normal":
                # プレイヤーのサイズが大きくなる
                player.status = "big"  # プレイヤーの状態をビッグに変更
                player.image = pygame.Surface([30, 50])
                player.image.fill(GREEN)
                # player.image = pygame.transform.rotozoom(pygame.image.load("fig/mario_big.png").convert(), 0, 2.92)
            self.kill()  # キノコを削除
            
        if not (self.rect.centerx == self.calculated_x and self.rect.centery > self.calculated_y):
            # ブロックとの衝突判定
            collided_blocks = pygame.sprite.spritecollide(self, blocks, False)
            for block in collided_blocks:
                # キノコが左からブロックに衝突した場合
                if self.speed_x < 0 and self.rect.right > block.rect.left:
                    self.rect.left = block.rect.right
                    self.speed_x *= -1  # 横方向の速度を反転 
                 # キノコが右からブロックに衝突した場合
                elif self.speed_x > 0 and self.rect.left < block.rect.right:
                    self.rect.right = block.rect.left - 3
                    print(self.speed_x)
                    self.speed_x *= -1  # 横方向の速度を反転
                    print(self.speed_x)

    # キノコの縦方向の衝突判定
    def check_vertical_collision(self, player, blocks):
        if player.rect.colliderect(self.rect):
            # ここにプレイヤーとの当たり判定の処理を追加
            if player.status == "normal":
                print("キノコとプレイヤーが衝突しました")
                # プレイヤーのサイズが大きくなる
                player.status = "big"  # プレイヤーの状態をビッグに変更
                player.image = pygame.Surface([40, 60])
                player.image.fill(GREEN)
                # player.image = pygame.transform.rotozoom(pygame.image.load("fig/mario_big.png").convert(), 0, 2.92)
            self.kill()  # キノコを削除

        if  not (self.rect.centerx == self.calculated_x and self.rect.centery > self.calculated_y):
            # ブロックとの衝突判定
            collided_blocks = pygame.sprite.spritecollide(self, blocks, False)
            for block in collided_blocks:
                if self.speed_y > 0 and self.rect.top < block.rect.bottom:
                    # キノコが下からブロックに衝突した場合
                    self.rect.bottom = block.rect.top
                    self.speed_y = 0
                elif self.speed_y < 0 and self.rect.bottom > block.rect.top:
                    # キノコが上からブロックに衝突した場合
                    self.rect.top = block.rect.bottom
                    self.speed_y = 0

        


# block_questionの衝突判定

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("マリオっぽいゲーム")
    clock = pygame.time.Clock()

    # 背景画像のロード
    bg_img = pygame.transform.rotozoom(pygame.image.load("fig/dot_map.png").convert(), 0, 2.92)
    bg_width = bg_img.get_width()
    bg_height = bg_img.get_height()

    

    all_sprites = pygame.sprite.Group()
    blocks = CustomGroup()  # ブロック用のカスタムグループ
    player = Player()
    mushroom = CustomGroup()  # キノコ用のカスタムグループ
    all_sprites.add(player)
    for i in BLOCK_NORMAL_POS:
        block = Block_nomal(i)
        all_sprites.add(block)
        blocks.add(block)
    for i in BLOCK_TRANSPARENT_POS:
        block = Block_transparent(i)
        all_sprites.add(block)
        blocks.add(block)
    for i in BLOCK_QUESTION_POS:
        block = Block_question(i, all_sprites, MUSHROOM_POS, mushroom)
        all_sprites.add(block)
        blocks.add(block)
    scroll_x = 0  # 背景のスクロール量

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speed_x = -5
                if event.key == pygame.K_RIGHT:
                    player.speed_x = 5
                if event.key == pygame.K_SPACE:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.speed_x < 0:
                    player.speed_x = 0
                if event.key == pygame.K_RIGHT and player.speed_x > 0:
                    player.speed_x = 0

        # ゲームループ
        player.update_x()  
        blocks.call_method("update_x", player)  # ブロックの横方向の更新
        mushroom.call_method("update_x" )  # キノコの横方向の更新
        mushroom.call_method("check_collision", player, blocks)  # キノコの横方向の衝突判定
        player.update_y()
        blocks.call_method("update_y", player)  # ブロックの縦方向の更新
        mushroom.call_method("update_y")  # キノコの縦方向の更新
        mushroom.call_method("check_vertical_collision", player, blocks)  # キノコの縦方向の衝突判定

        # プレイヤーが画面中央より右に行ったら背景をスクロール
        center_x = SCREEN_WIDTH // 2
        if player.world_x > center_x:
            scroll_x = player.world_x - center_x
        else:
            scroll_x = 0  # プレイヤーが中央より左にいる場合はスクロールしない

        # 背景の範囲外に行かないように制限
        max_scroll = bg_width - SCREEN_WIDTH
        if scroll_x > max_scroll:
            scroll_x = max_scroll
        if scroll_x < 0:
            scroll_x = 0  # 念のため再確認

        # プレイヤーのワールド座標が0未満にならないようにする
        if player.world_x < 0:
            player.world_x = 0
        

        if player.world_x > bg_width - player.rect.width:
            player.world_x = bg_width - player.rect.width

        # プレイヤーの画面上のx座標を調整
        if player.world_x < center_x:
            player.rect.x = player.world_x
        elif player.world_x > bg_width - (SCREEN_WIDTH - center_x):
            # スクロールが最大になったら、プレイヤーは右端で止まる
            player.rect.x = player.world_x - scroll_x
            # if player.rect.x > SCREEN_WIDTH:
            #     player.rect.x = SCREEN_WIDTH
        else:
            player.rect.x = center_x

        # 描画
        if scroll_x >= 0:
            screen.blit(bg_img, (-scroll_x, 0))

        # --- ここから修正 ---
        # キノコをスクロールに合わせて描画
        for mush in mushroom:
            mush_screen_rect = mush.rect.copy()
            mush_screen_rect.x -= scroll_x
            screen.blit(mush.image, mush_screen_rect)
        # ブロックをスクロールに合わせて描画
        for block in blocks:
            block_screen_rect = block.rect.copy()
            block_screen_rect.x -= scroll_x
            screen.blit(block.image, block_screen_rect)
        # プレイヤーを描画
        if player.status != "goal":
            screen.blit(player.image, player.rect)
        # --- ここまで修正 ---

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()