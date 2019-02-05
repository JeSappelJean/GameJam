import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((16*2,20*2))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumpCount = 0
        self.jumping = False

    def jump(self):
        #self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        #self.rect.x -=1
        if self.jumpCount == 0:
            self.jumping == False

        if self.jumping and self.jumpCount != 0:
            self.vel.y = -PLAYER_JUMP
            self.jumpCount -= 1



    def jump_reverse(self, droite):
        if droite:
            sens = 1
        else :
            sens = -1

        self.vel.y = -PLAYER_JUMP
        self.acc.x -= 22 * sens

        self.vel += self.acc

        self.pos += self.vel  + 0.5 * self.acc

        self.rect.midbottom = self.pos





    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
                self.acc.x -= PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x += PLAYER_ACC
        


        #appliquer la friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        #équation de mouvement
        self.vel += self.acc

        self.pos += self.vel  + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def get_platform(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if self.vel.y > 0 and hits:
            self.platfrom = hits[0]
        else :
            self.platfrom = 0


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x , y, w, h):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w,h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
