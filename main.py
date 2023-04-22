#imports
from pygame import*
from button import Button

#window
window = display.set_mode((700,500))
display.set_caption("Woodcutter-Simulator")
#class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, x, y, w, h, player_speed, dmg):
        super().__init__(player_image, x, y, w, h, player_speed)
        self.dmg = dmg

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.image = transform.scale(image.load('player_move_L_1.png'), (100, 50))
            self.rect.x -= self.speed
            self.image = transform.scale(image.load('player_move_L_2.png'), (100, 50))

        if keys_pressed[K_RIGHT] and self.rect.x < 700:
            self.image = transform.scale(image.load('player_move_R_1.png'), (100, 50))
            self.rect.x += self.speed
            self.image = transform.scale(image.load('player_move_R_2.png'), (100, 50))

class Tree(GameSprite):
    def __init__(self, player_image, x, y, w, h, player_speed, tree_hp):
        super().__init__(player_image, x, y, w, h, player_speed)
        self.hp = tree_hp

    def life_bar_lvl_1(self):
        if self.hp <= 0:
            self.hp = 0
            self.kill()

money = 1
class Money_coin(GameSprite):
    def money_update(self):
        global money
        if money >= 10000:
            money = 10000
#changes
FPS = 60
game = True
clock = time.Clock()
run = False
#class realese
player1 = Player("player.png", 350, 375, 100, 50, 2, 1)
tree_lvl_1 = Tree("Tree_lvl_2.png", 550, 375, 100, 50, 10, 10)
gold_coin = Money_coin("gold_icon.png", 575, 0, 25, 25, 1)
#btns
btn_start = Button(200, 200, 100, 50, "btn_start.png")
btn_exit = Button(200,200, 100, 50, "btn_exit.png")
#Text
font.init()
font = font.SysFont('Arial', 20)
#Background music
mixer.init()
mixer.music.load("forest_sounds.ogg")
mixer.music.play(-1)
#background
background_image = image.load('background.jpg')
background = transform.scale(background_image, (700,500))
#while
while game:
    #events
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = not run

    if run:
        #logic game
        window.fill(255,0,0)
        player1.reset()
        tree_lvl_1.reset()
        #money_show
        gold_coin.money_update()
        gold_coin.reset()
        #bars
        text = font.render(str(money) + "cash", 1, (255,255,0))
        window.blit(text, (600,0))
        hp_text = font.render("Hp:" + str(tree_lvl_1.hp), 1, (255,255,255))
        window.blit(hp_text, (550,350))

        player1.update()
        tree_lvl_1.life_bar_lvl_1()
        #ifs
        for e in event.get():
            for e in event.get():
                if e.type == pygame.KEYUP:
                    if e.key == K_LEFT or e.key == K_RIGHT:
                        player1.image = transform.scale(image.load('player.png'), (100, 50))

        if sprite.collide_rect(tree_lvl_1, player1):
            tree_lvl_1.hp -= player1.dmg
            money += 1

    else:
        #menu game
        window.fill(0,0,0)
        if btn_start.draw(window):
            run = True
        if btn_exit.draw(window):
            run = False


    
    display.update()
    clock.tick(FPS)