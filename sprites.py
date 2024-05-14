# This file was created by Alessandro Calioni
# This code was inspired by Zelda and informed by Chris Bradfield

import pygame as pg
from settings import *
from random import choice
from random import randint
from os import path
PHASE_DURATION = 5000


vec =pg.math.Vector2
# create a class for player
class Player(pg.sprite.Sprite):
    # define __init__(self)
    # This section below is basically the function of creating the bounds of the "map" I think
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vs, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.hitpoints = 100
        self.phase_through_walls_active = False
        self.phase_through_walls_start_time = 0
        self.color_timer = 0  # Timer to control color change
        self.colors = [RED, GREEN, BLUE, YELLOW, PURPLE]  # List of colors

    def change_color(self):
        # Change color to a random color from the list
        self.image.fill(choice(self.colors))
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_s]:
            self.vy = self.speed
        if keys[pg.K_DOWN] or keys[pg.K_w]:
            self.vy = -self.speed
        if self.vx !=0 and self.vy !=0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        # if keys[pg.K_o]:
        #     self.player1.change_color()
        
    
                
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                self.speed += 50
            if str(hits[0].__class__.__name__) == "HealthPotion":
                print(hits[0].__class__.__name__)
                self.hitpoints += 25
            if str(hits[0].__class__.__name__) == "Mob":
                print(hits[0].__class__.__name__)
                print("collided with mob")
                self.hitpoints -= 1
            # if self.hitpoints == 0:
            #     quit(self)
                         

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.healthpotion, True)

        if self.phase_through_walls_active:
            current_time = pg.time.get_ticks()
            if current_time - self.phase_through_walls_start_time >= PHASE_DURATION:
                self.deactivate_phase_through_walls()
        # # Control color change timing
        # if pg.time.get_ticks() - self.color_timer > 300:  # Change color every 0.3 seconds
        #     self.change_color()
        #     self.color_timer = pg.time.get_ticks()  # Reset timer

    # The following was made with the aid of chat GPT
    def activate_phase_through_walls(self):
        self.phase_through_walls_active = True
        self.phase_through_walls_start_time = pg.time.get_ticks()

    def deactivate_phase_through_walls(self):
        self.phase_through_walls_active = False
        self.phase_through_walls_start_time = 0    

    def collide_with_walls(self, dir):
        if not self.phase_through_walls_active:
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                    self.vx = 0
                    self.rect.x = self.x
                # for wall in hits:
                #     for wall in hits:
                #         wall.change_color()  # Call the change_color method of the wall
                #         wall.color_timer = pg.time.get_ticks()  # Start color change timer
                #         self.vx = 0
                #         self.x = wall.rect.x if self.vx > 0 else wall.rect.right
                #         self.rect.x = self.x
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                    self.vy = 0
                    self.rect.y = self.y
                # for wall in hits:
                #     wall.change_color()  # Call the change_color method of the wall
                #     wall.color_timer = pg.time.get_ticks()  # Start color change timer
                #     self.vy = 0
                #     self.y = wall.rect.y if self.vy > 0 else wall.rect.bottom
                #     self.rect.y = self.y

# we created a class for wall and used the similar function for the class player
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.game = game
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    #     # self.color_timer = 0  # Timer to control color change
    #     # self.colors = [PINK, ORANGE, CYAN, MAGENTA]  # List of colors for wall change
    #     # self.original_color = BLUE

    # def change_color(self):
    #     # Change color to a random color from the list
    #     self.image.fill(choice(self.colors))

    # def update(self):
    #     # Control color change timing
    #     if pg.time.get_ticks() - self.color_timer > 2000:  # Change color for 2 seconds
    #         self.image.fill(self.original_color)  # Revert color back to original
    #         self.color_timer = 0


class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.game = game
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class HealthPotion(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.healthpotion
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 100
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player1.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player1.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player1.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player1.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')


class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 1000
        self.speed = 450
        self.chasing = False
    def sensor(self):
        if abs(self.rect.x - self.game.player1.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player1.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    def collide_with_walls(self, dir):
        if dir == 'x':
        # Since we have the (self, self.game.walls, TRUE) set to TRUE, that means when it collides with the wall the wall will disappear
            hits = pg.sprite.spritecollide(self, self.game.walls, True)
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, True)
    def update(self):
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player1.rect.center - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
  
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.collide_with_walls('x')
            self.collide_with_walls('y')
            # self.hit_rect.centerx = self.pos.x        




