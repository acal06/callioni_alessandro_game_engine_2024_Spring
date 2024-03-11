# This file was created by Alessandro Calioni
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *

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
        self.speed = 450
    

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if self.vx !=0 and self.vy !=0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        

    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False

    # def collide_with_walls(self, dir):
    #     if dir == 'x':
    #         hits = pg.sprite.spritecollide(self, self.game.walls, False)
    #         if hits:
    #             if self.vx > 0:
    #                 self.x = hits[0].rect.left - self.width
    #             if self.vx < 0:
    #                 self.x = hits[0].rect.right
    #             self.vx = 0
    #             self.rect.x = self.x
    #     if dir == 'y':
    #         hits = pg.sprite.spritecollide(self, self.game.walls, False)
    #         if hits:
    #             if self.vy > 0:
    #                 self.y = hits[0].rect.bottom - self.height
    #             if self.vy < 0:
    #                 self.y = hits[0].rect.top
    #             self.vy = 0
    #             self.rect.y = self.y

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_coins(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.coins, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.coins, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.bottom - self.height
                if self.vy < 0:
                    self.y = hits[0].rect.top
                self.vy = 0
                self.rect.y = self.y
                

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                self.speed += 300
            if str(hits[0].__class__.__name__) == "Mob":
                print(hits[0].__class__.__name__)
                print("collided with mob")
            




# Now we fixed collision problem by finding that it wasn't colliding with the walls vertically. Below is the old version and below this commented bit is the new 
                # version copied from Github
    # def update(self):
    #     self.get_keys()
    #     self.x += self.vx *self.game.dt
    #     self.y += self.vy *self.game.dt
    #     self.rect.x = self.x
    #     # add collision later
    #     self.collide_with_walls('x')
    #     self.rect.y = self.y 
    #     self.collide_with_group(self.game.coins, True)
    #     # add collision later
    #     # if self.collide_with_coins():
    #     #     self.moneybag += 1
    #     # coin_hits = pg.sprite.spritecollide(self, self.game.coins, True)
    #     # if coin_hits:
    #     #     self.moneybag += 1

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

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
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
        self.image.fill(YELLOW)
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
        self.speed = 1
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


# class Mob2(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.mobs
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.rect = self.image.get_rect()
#         self.pos = vec(x, y) * TILESIZE
#         self.vel = vec(0, 0)
#         self.acc = vec(0, 0)
#         self.rect.center = self.pos
#         self.rot = 0
#         # added
#         self.speed = 150
#     def update(self):
#         self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
#         self.rect.center = self.pos
#         self.acc = vec(self.speed, 0).rotate(-self.rot)
#         self.acc += self.vel * -1
#         self.vel += self.acc * self.game.dt
#         self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
#         # self.hit_rect.centerx = self.pos.x
#         collide_with_walls(self, self.game.walls, 'x')
#         # self.hit_rect.centery = self.pos.y
#         collide_with_walls(self, self.game.walls, 'y')
#         # self.rect.center = self.hit_rect.center
#         # if self.health <= 0:
#         #     self.kill()
