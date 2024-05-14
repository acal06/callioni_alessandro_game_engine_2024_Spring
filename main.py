# This file was created by: Alessandro Callioni
# added this commnet to prove github is listening...
# imports the pygme as pg and imports settings code
'''
moving enemies
coin counter
player death
health bar
speed power up
health powerup
 

Beta version:
Fix level2

Release version:
Phase through walls ability with spacebar - requries collision, timer, and ability changes so the player can go through walls without colliding with them
'''


import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"
PHASE_DURATION = 5000


# we create a variable called game
class Game:
    # defines properties to self
    def __init__(self):
        # initiate pygame
        pg.init()
        # set up screen
        self.screen  = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        # set up game speed
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'level1.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.healthpotion = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == '2':
                    print("a coin at", row, col)
                    Coin(self, col, row)
                if tile == '3':
                    print("a powerup at", row, col)
                    PowerUp(self, col, row)
                if tile == 'M':
                    print("a mob at", row, col)
                    Mob(self, col, row)
                if tile == 'N':
                    print("a mob at", row, col)
                    Mob(self, col, row)
                if tile == 'M':
                    Mob2(self, col, row)
                if tile == 'H':
                    HealthPotion(self, col, row)
                if tile == 'P':
                    self.player1 = Player(self, col, row)
    # makes it so that when we start the game its choosing to start from the first level text t start with
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    # The following makes it so that when we change to level 2 it prints all the features where the associated letters are with the map
    def test_method(self):
        print("I can be called from Sprites...")
    # added level change method
    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.player1.moneybag = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # repopulate the level with stuff
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == '2':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'N':
                    Mob(self, col, row)
                if tile == 'M':
                    Mob2(self, col, row)
                if tile == '3':
                    PowerUp(self, col, row)
                if tile == 'H':
                    HealthPotion(self, col, row)

    # define run
    def run(self):
        # 
        self.playing = True
        while self.playing:
           self.dt = self.clock.tick(FPS) / 1000 
           self.events()
           self.update()
           self.draw()
    def quit(self):
        pg.quit()
        sys.exit()
    # The following makes it so that when the player collects the sixth coin the level changes to level 2
    # it also makes sure that if the player's health reaches zero, then it ends the game
    def update(self):
        self.all_sprites.update()
        if self.player1.moneybag > 5:
            self.change_level(LEVEL2)
        if self.player1.hitpoints == 0:
            self.show_end_screen()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

# defining draw_health_bar
    def draw_health_bar(surf, x, y, pct):
        if pct <0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surf, GREEN, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('comicsans')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)


    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player1.moneybag), 64, WHITE, 1, 1)
        # draw the healthbar above the player and connect it to player hitpoints
        draw_health_bar(self.screen, self.player1.rect.x, self.player1.rect.y, self.player1.hitpoints)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player1.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player1.move(dx=+1)
                if event.key == pg.K_UP:
                    self.player1.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player1.move(dy=+1)
                if event.key == pg.K_SPACE:
                    self.player1.activate_phase_through_walls()
                    print("SPACEBAR")
# basically all of this above lets us use the keys to move our character around
        # The following was made with the help and assistance of chat GPT
        if self.player1.phase_through_walls_active:
            current_time = pg.time.get_ticks()
            PHASE_DURATION = 5000
            if current_time - self.player1.phase_through_walls_start_time >= PHASE_DURATION:
                self.player1.deactivate_phase_through_walls()

        PHASE_DURATION = 5000  # Duration of the phase through walls ability in milliseconds (5 seconds)



# defininig the start screen
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen", 24, WHITE, 11, 10)
        pg.display.flip()
        self.wait_for_key()

# defininig the start screen
    def show_end_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Game Over", 24, WHITE, 11, 10)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting: 
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
                    # when the key is released after being pressed the game no longer waits and the title screen goes away

def draw_health_bar(surf, x, y, pct):
    if pct <0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    # we use this to fill the area defined by the health bar
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


# Instantiate the game...
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()