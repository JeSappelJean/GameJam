import pygame as pg
import random
from settings import *
from sprites import *
from os import path
import string


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
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()


    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.spritesheet_car = Spritesheet(path.join(img_dir, SPRITESHEET_CAR),SIZE_CAR)
        self.spritesheet_plat = Spritesheet(path.join(img_dir, SPRITESHEET_PLAT),SIZE_PLAT)
        self.level1 = Niveau(path.join(img_dir,"test.txt"))


    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.player = Player(self)
        self.draw_level()
        self.run()

    def run(self):
        #Boucle du jeu
        self.playing = True
        while self.playing:
            time =self.clock.tick(FPS)
            self.time_elapsed += 1
            self.events()
            self.update()
            self.draw()

    def update(self):

        self.all_sprites.update()
        nbCollideBottom = 0
        nbCollideTop = 0
        nbCollideLeft = 0
        nbCollideRight = 0

        if self.player.vel.y != 0:

            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.collidepoint(self.player.rect.midbottom):
                        nbCollideBottom += 1
                    if hit.rect.collidepoint(self.player.rect.midtop):
                        nbCollideTop += 1
                    if hit.rect.collidepoint(self.player.rect.midright):
                        nbCollideRight += 1
                    if hit.rect.collidepoint(self.player.rect.midleft):
                        nbCollideLeft += 1
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit

                if len(hits) > 4:
                    wall = True
                else:
                    wall = False

                if self.player.vel.y > 0 and nbCollideBottom > 0 :
                    self.player.pos.y = lowest.rect.top +1
                    self.player.vel.y = 0
                    self.player.jumping = True
                    self.player.jumpCount = 2


                if self.player.vel.y < 0 and nbCollideTop > 0:
                    self.player.vel.y = 0
                    self.player.pos.y = hits[0].rect.bottom + self.player.image.get_height()


        if self.player.vel.x != 0 :
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if hits[0].rect.collidepoint(self.player.rect.midbottom) and len(hits) != 1:
                    ind = 1
                else:
                    ind = 0


                for hit in hits:
                    if hit.rect.collidepoint(self.player.rect.midbottom):
                        nbCollideBottom += 1
                    if hit.rect.collidepoint(self.player.rect.midtop):
                        nbCollideTop += 1
                    if hit.rect.collidepoint(self.player.rect.midright):
                        nbCollideRight += 1
                    if hit.rect.collidepoint(self.player.rect.midleft):
                        nbCollideLeft += 1
                if self.player.vel.x > 0 and nbCollideRight > 0:
                    self.player.vel.x = 0
                    self.player.acc.x = 0
                    self.player.pos.x = hits[ind].rect.left - self.player.image.get_width()/2
                    self.player.slidingL = True
                    keys = pg.key.get_pressed()
                    if keys[pg.K_SPACE] :
                        self.player.jump_reverse(True)
                if self.player.vel.x < 0 and nbCollideLeft > 0:
                    self.player.vel.x = 0
                    self.player.acc.x = 0
                    self.player.pos.x = hits[ind].rect.right + self.player.image.get_width()/2
                    self.player.slidingR = True
                    keys = pg.key.get_pressed()
                    if keys[pg.K_SPACE]:
                            self.player.jump_reverse(False)

        if self.player.rect.top > HEIGHT:
            self.playing =False


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
        self.screen.fill(BG)
        self.all_sprites.draw(self.screen)
        self.draw_text("Speed : "+str(abs(round(self.player.vel.x, 1))), 22, WHITE, 50, 50)
        self.screen.blit(self.player.image, self.player.rect)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_level(self) :
        self.level1.generate()
        num_ligne = 0
        for line in self.level1.struct:
            nume_case = 0
            for sprite in line :
                x = nume_case * 8*SIZE_PLAT
                y = num_ligne * 8*SIZE_PLAT
                if sprite == '1':
                    Platform(self,x,y,0)
                if sprite == '3':
                    Platform(self,x,y,1)
                if sprite == '5':
                    Platform(self,x,y,2)
                if sprite == '7':
                    Platform(self,x,y,3)
                if sprite == '9':
                    Platform(self,x,y,4)
                if sprite == 'b':
                    Platform(self,x,y,5)
                if sprite == 'd':
                    Platform(self,x,y,6)
                if sprite == 'f':
                    Platform(self,x,y,7)
                if sprite == 'h':
                    Platform(self,x,y,8)
                if sprite == 'j':
                    Platform(self,x,y,9)
                if sprite == 'j':
                    Platform(self,x,y,10)
                if sprite == 'l':
                    Platform(self,x,y,11)
                if sprite == 'n':
                    Platform(self,x,y,12)
                if sprite == 'p':
                    Platform(self,x,y,13)
                if sprite == 'r':
                    Platform(self,x,y,14)
                if sprite == 't':
                    Platform(self,x,y,15)
                if sprite == 'v':
                    Platform(self,x,y,15)
                if sprite == 'x':
                    Platform(self,x,y,16)
                nume_case += 1
            num_ligne += 1

g = Game()

while g.running:
    g.new()

pg.quit()
