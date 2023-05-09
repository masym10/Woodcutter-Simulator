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
        #cooldown
        global cooldown_tracker
        cooldown_tracker += clock.get_time()
        if cooldown_tracker > cd:
            cooldown_tracker = 0
        
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE] and cooldown_tracker == 0:
            self.image = transform.scale(image.load(player_axe_images[0]), (100, 50))
            self.attack = True

class Tree(GameSprite):
    def __init__(self, player_image, x, y, w, h, player_speed, tree_hp):
        super().__init__(player_image, x, y, w, h, player_speed)
        self.hp = tree_hp

    def life_bar_lvl_1(self):
        if self.hp <= 0:
            self.hp = 0
            global max_hp


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
money = 0
max_hp = 50
kill_tree = 0
max_kill_tree = 5
max_tree = 5
money_drop = 5
cooldown_tracker = 0
cd = 1200           

#class realese
player1 = Player("player_R.png", 350, 375, 100, 50, 2, 1)
gold_coin = Money_coin("gold_icon.png", 575, 0, 25, 25, 1)
tree = Tree("Tree_lvl_1.png", 550, 375, 100, 50, 10, 10)

#btns
btn_start = Button(300, 200, 100, 50, "btn_start.png")
btn_exit = Button(300, 275, 100, 50, "btn_exit.png")
btn_sound = Button(650, 450, 100, 50, "btn_sound.png")
btn_mute = Button(650, 400, 100, 50, "btn_mute.png")
btn_shop = Button(70, 50, 50, 25, "btn_shop.png")
btn_buy =  Button(200, 50, 50, 25, "btn_buy.png")
btn_buy2 = Button(400, 50, 50, 25, "btn_buy.png.")
btn_buy3 = Button(200, 100, 50, 25, "btn_buy.png.")
btn_buy4 = Button(400, 100, 50, 25, "btn_buy.png.")
btn_buy5 = Button(200, 150, 50, 25, "btn_buy.png.")
btn_buy6 = Button(400, 150, 50, 25, "btn_buy.png.")
btn_close = Button(5, 5, 50, 25, "btn_close.png")

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
#player settings
player_axe_images = [
    "player_axe_lvl_1.png", "player_axe_lvl_2.png", "player_axe_lvl_3.png", "player_axe_lvl_4.png", "player_axe_lvl_5.png",
    "player_axe_lvl_6.png"
    ]

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
        kill_tree_text = font.render("Tree:" + str(kill_tree), 1, (255, 0, 0))
        window.blit(kill_tree_text, (580, 50))

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
            now_tree = randint(1, max_tree)
            kill_tree += 1
            if kill_tree == max_kill_tree:
                note_text = font.render("You need buy new axe.", 1, (255, 0, 0))
                window.blit(note_text, (350, 250))
                cooldown_tracker = 99999
                
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
            money += money_drop

        if btn_shop.draw(window):
            open = True
        #shop interface
        if open == True:
            if btn_buy.draw(window):
                if money >= 25:
                    player1.dmg += 2
                    player_axe_images.remove("player_axe_lvl_1.png")
                    money -= 25
                    kill_tree = 0
                    if player1.image == "player_level_axe_2":
                        cooldown_tracker = 0
                else:
                    money1 = money
                    need_money = money - 25
                    error_buy = font.render(f"You dont have need money " + str(need_money), 1, (255, 0, 0))
                    window.blit(error_buy, (200, 200))

            if btn_buy2.draw(window):
                if money >= 250:
                    cd = 1100
                    player1.dmg += 5
                    player_axe_images.remove("player_axe_lvl_2.png")
                    money -= 250
                    kill_tree = 0

                else:
                    money2 = money
                    need_money2 = money - 250
                    error_buy2 = font.render(f"You dont have need money " + str(need_money2), 1, (255, 0, 0))
                    window.blit(error_buy2, (200, 200))
            
            if btn_buy3.draw(window):
                if money >= 500:
                    cd = 1000
                    player1.dmg += 8
                    player_axe_images.remove("player_axe_lvl_3.png")
                    money -= 500
                    kill_tree = 0
                else:
                    money1 = money
                    need_money3 = money - 500
                    error_buy3 = font.render(f"You dont have need money " + str(need_money3), 1, (255, 0, 0))
                    window.blit(error_buy3, (200, 200))

            if btn_buy4.draw(window):
                if money >= 750:
                    cd = 900
                    player1.dmg += 11
                    player_axe_images.remove("player_axe_lvl_4.png")
                    money -= 750
                    kill_tree = 0
                else:
                    money4 = money
                    need_money4 = money - 750
                    error_buy4 = font.render(f"You dont have need money " + str(need_money4), 1, (255, 0, 0))
                    window.blit(error_buy4, (200, 200))

            if btn_buy5.draw(window):
                if money >= 1000:
                    cd = 800
                    player1.dmg += 15
                    player_axe_images.remove("player_axe_lvl_5.png")
                    money -= 1000
                    kill_tree = 0
                else:
                    money5 = money
                    need_money = money - 1000
                    error_buy5 = font.render(f"You dont have need money " + str(need_money), 1, (255, 0, 0))
                    window.blit(error_buy5, (200, 200))

            if btn_buy6.draw(window):
                if money >= 2500:
                    cd = 400
                    player1.dmg += 30
                    player_axe_images.remove("player_axe_lvl_5.png")
                    money -= 2500
                    kill_tree = 0
                else:
                    money6 = money
                    need_money = money - 2500
                    error_buy6 = font.render(f"You dont have need money " + str(need_money), 1, (255, 0, 0))
                    window.blit(error_buy6, (200, 200))


            if btn_close.draw(window):
                open =False
                
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