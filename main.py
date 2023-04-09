#imports
from pygame import*

#window
window = display.set_mode((700,500))
#class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, x, y, w, h, player_speed, dmg):
        super().__init__(player_image, x, y, w, h, player_speed)
        self.dmg = dmg

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 700 - self.image.get_width():
            self.rect.x += self.speed

class Tree(GameSprite):
    def life_bar_lvl_1(self):
        global hp 
        hp = 10
        if hp <= 0:
            hp = 0
            self.reset()
#changes
FPS = 60
game = True
clock = time.Clock()
#class realese
player1 = Player("player.png", 50, 350, 100, 50, 2, 1)
tree_lvl_1 = Tree("Tree_lvl_1.png", 100, 350, 100, 50, 50)
#while
while game:
    #events
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill((255,20,230))
    player1.reset()
    tree_lvl_1.reset()

    player1.update()
    tree_lvl_1.life_bar_lvl_1()

    if sprite.collide_rect(player1, tree_lvl_1):
        hp -= player1.dmg
    
    display.update()
    clock.tick(FPS)