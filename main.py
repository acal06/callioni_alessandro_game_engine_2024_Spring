# This file was created by: Alessandro Callioni

# imports the pygme as pg and imports settings code
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

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
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
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
              

        self.player1 = Player(self, 1, 1)
        self.all_sprites.add(self.player1)
        for x in range(10, 20):
           Wall(self, x, 5)
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

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

# 
            
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
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
# basically all of this above lets us use the keys to move our character around
            
            




# Instantiate the game...
g = Game()
# use game method run to run
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()