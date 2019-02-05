import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        pg.init()
        #Audio
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.time_elapsed = 0
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        Platform(self, 0, HEIGHT - 40, WIDTH/3, 400)
        Platform(self, WIDTH/2, HEIGHT - 40, WIDTH/2, 400)
        Platform(self, WIDTH-100, 100, 100, 800)
        Platform(self, WIDTH-350, 200, 100, 400)
        self.run()

    def run(self):
        #Boucle du jeu
        self.playing = True
        while self.playing:
            time =self.clock.tick(FPS)
            self.time_elapsed += 1
            print(abs(self.player.vel.x))
            self.events()
            self.update()
            self.draw()

    def update(self):

        self.all_sprites.update()
        if self.player.vel.y != 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if self.player.vel.y > 0 and (hits[0].rect.collidepoint(self.player.rect.midbottom)):
                    self.player.pos.y = hits[0].rect.top +1
                    self.player.vel.y = 0
                    self.player.jumping = True
                    self.player.jumpCount = 2

                if self.player.vel.y < 0 and (hits[0].rect.collidepoint(self.player.rect.midtop)):
                    self.player.vel.y = 0
                    self.player.pos.y = hits[0].rect.bottom + self.player.image.get_height()


        if abs(self.player.vel.x) != 0 :
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)

            if hits:
                if hits[0].rect.collidepoint(self.player.rect.midbottom) and len(hits) != 1:
                    ind = 1
                else:
                    ind = 0
                if self.player.vel.x > 0 and (hits[ind].rect.collidepoint(self.player.rect.midright)):
                    self.player.vel.x = 0
                    self.player.acc.x = 0
                    self.player.pos.x = hits[ind].rect.left - self.player.image.get_width()/2
                    self.player.slidingL = True
                    keys = pg.key.get_pressed()
                    if keys[pg.K_SPACE]:
                        self.player.jump_reverse(True)
                if self.player.vel.x < 0 and (hits[ind].rect.collidepoint(self.player.rect.midleft)):
                    self.player.vel.x = 0
                    self.player.acc.x = 0
                    self.player.pos.x = hits[ind].rect.right + self.player.image.get_width()/2
                    self.player.slidingR = True
                    keys = pg.key.get_pressed()
                    if keys[pg.K_SPACE]:
                            self.player.jump_reverse(False)


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()


    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        pg.display.flip()

g = Game()

while g.running:
    g.new()

pg.quit()
