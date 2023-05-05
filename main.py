#imports
from pygame import*
from button import Button
from random import randint

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
        self.attack = False

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.image = transform.scale(image.load('player_L.png'), (100, 50))
            self.rect.x -= self.speed

        if keys_pressed[K_RIGHT] and self.rect.x < 700:
            self.image = transform.scale(image.load('player_R.png'), (100, 50))
            self.rect.x += self.speed

    def attack_axe(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            self.image = transform.scale(image.load('player_axe_lvl_1.png'), (100, 50))
            self.attack = True

class Tree(GameSprite):
    def __init__(self, player_image, x, y, w, h, player_speed, tree_hp):
        super().__init__(player_image, x, y, w, h, player_speed)
        self.hp = tree_hp

    def life_bar_lvl_1(self):
        if self.hp <= 0:
            self.hp = 0
            global max_hp

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
player1 = Player("player_R.png", 350, 375, 100, 50, 2, 1)
gold_coin = Money_coin("gold_icon.png", 575, 0, 25, 25, 1)
tree = Tree("Tree_lvl_1.png", 550, 375, 100, 50, 10, 10)


#btns
btn_start = Button(300, 200, 100, 50, "btn_start.png")
btn_exit = Button(300, 275, 100, 50, "btn_exit.png")
btn_sound = Button(650, 450, 100, 50, "btn_sound.png")
btn_mute = Button(650, 400, 100, 50, "btn_mute.png")

#Text
font.init()
font = font.SysFont('Arial', 20)

#Background music
mixer.init()
mixer.music.load("forest_sounds.ogg")

#background
background_image = image.load('background.jpg')
background = transform.scale(background_image, (700, 500))
background_menu_image = image.load('background_menu.jpg')
background_menu = transform.scale(background_menu_image, (700, 500))

max_hp = 50
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
        window.blit(background, (0, 0))
        player1.reset()
        player1.attack_axe()
        tree.reset()

        #money_show
        gold_coin.money_update()
        gold_coin.reset()

        #bars
        text = font.render(str(money) + "cash", 1, (255,255,0))
        window.blit(text, (600,0))
        hp_text = font.render("Hp:" + str(tree.hp), 1, (255,255,255))
        window.blit(hp_text, (550,350))

        player1.update()
        tree.life_bar_lvl_1()
        #ifs
        if player1.attack == True:
            if sprite.collide_rect(player1, tree):
                tree.hp -= player1.dmg
                player1.attack = False
        else:
            player1.image = transform.scale(image.load('player_R.png'), (100, 50))

        if tree.hp <= 0:
            max_tree = 5
            now_tree = randint(1, max_tree)

            if now_tree == 1:
                tree.image = transform.scale(image.load('Tree_lvl_1.png'), (100, 50))
            if now_tree == 2:
                tree.image = transform.scale(image.load('Tree_lvl_2.png'), (100, 50))
            if now_tree == 3:
                tree.image = transform.scale(image.load('Tree_lvl_3.png'), (100, 50))
            if now_tree == 4:
                tree.image = transform.scale(image.load('Tree_lvl_4.png'), (100, 50))
            if now_tree == 5:
                tree.image = transform.scale(image.load('Tree_lvl_5.png'), (100, 50))

            max_hp += 10 
            tree.hp = randint(10, max_hp)
            money += 5 

    else:
        #menu game
        window.blit(background_menu, (0, 0))
        if btn_start.draw(window):
            run = True

        if btn_exit.draw(window):
            game = False

        if btn_sound.draw(window):
            mixer.music.play(-1)

        if btn_mute.draw(window):
            mixer.music.pause()


            
    display.update()
    clock.tick(FPS)