import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from random import *
import string


class Game:
    def __init__(self):
        pg.init()
        #Audio
        self.start = True
        self.freeplay = False
        self.score = 0
        pg.mixer.init()
        self.level = 0
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.dash_time = 0
        self.time_elapsed = 0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()



    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        self.map_dir = path.join(self.img_dir, 'map')
        self.sound_dir = path.join(self.dir, 'music')
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, 'jump_sound.ogg'))

        self.damage_sound = pg.mixer.Sound(path.join(self.sound_dir, 'damage_sound.ogg'))
        self.start_screen_music = pg.mixer.Sound(path.join(self.sound_dir, 'start_screen_music.ogg'))
        self.portal = pg.mixer.Sound(path.join(self.sound_dir, 'portal_sound.ogg'))
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.hightscore = int(f.read())
            except:
                self.hightscore = 0
        self.spritesheet_car = Spritesheet(path.join(self.img_dir, SPRITESHEET_CAR),SIZE_CAR)
        self.spritesheet_plat = Spritesheet(path.join(self.img_dir, SPRITESHEET_PLAT),SIZE_PLAT)
        self.spritesheet_button = Spritesheet(path.join(self.img_dir, SPRITESHEET_BUTTON),SIZE_BUTTON)

    def new(self):

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.lave = pg.sprite.Group()
        self.level_end = pg.sprite.Group()
        self.ressorts = pg.sprite.Group()
        self.run()

    def run(self):
        #Boucle du jeu
        self.playing = True
        self.load_map()
        self.draw_level()
        if self.start == True :
            self.start = False
            pg.mixer.music.load(path.join(g.sound_dir, 'game_music.ogg'))
            pg.mixer.music.load(path.join(g.sound_dir, 'game_music.ogg'))
            pg.mixer.music.play(loops=-1)

        while self.playing:

            time = self.clock.tick(FPS)
            self.time_elapsed += 1
            self.dash_time += 1

            self.events()
            self.update()
            self.draw()
        pg.mixer.fadeout(500)

    def load_map(self):
        if self.freeplay == True :
            random_level = randint(0, len(LEVEL_LIST)-1)
            self.current_level = Niveau(path.join(self.map_dir,LEVEL_LIST[random_level]))
        else:
            self.current_level = Niveau(path.join(self.map_dir,LEVEL_LIST[self.level]))
        self.player = Player(self, self.current_level.x_start, self.current_level.y_start)
        if self.current_level.grav == 1:
            self.player.gravity = True
        else :
            self.player.gravity = False

    def update(self):
        if self.freeplay == False :
            if self.time_elapsed/100 > 180:
                if self.score > self.hightscore:
                    self.hightscore = self.score
                    with open(path.join(self.dir, HS_FILE), 'w') as f:
                        f.write(str(self.score))
                self.time_elapsed = 0
                self.level = 0
                self.playing = False

        keys = pg.key.get_pressed()
        self.all_sprites.update()
        nbCollideBottom = 0
        nbCollideTop = 0
        nbCollideLeft = 0
        nbCollideRight = 0
        end_level = pg.sprite.spritecollide(self.player, self.level_end, False)
        hit_ressors = pg.sprite.spritecollide(self.player, self.ressorts, False)
        if hit_ressors:
            self.player.vel.y = -20

        if end_level :
            self.level += 1
            if self.level > len(LEVEL_LIST) -1 :
                self.level = 0
            self.score += 10
            self.portal.play()
            for plat in self.all_sprites:
                plat.kill()
            self.load_map()
            self.draw_level()
            self.all_sprites.update()


        #Dead
        dead = pg.sprite.spritecollide(self.player, self.lave, False)
        if dead:
            self.player.vel.x = 0
            self.player.acc.x = 0
            self.player.pos.x = self.current_level.x_start
            self.player.pos.y = self.current_level.y_start
            self.damage_sound.play()

        if self.player.vel.y != 0:

            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if self.player.rect.top < 0 :
                self.player.vel.y = 0
                self.player.pos.y = self.player.image.get_height()

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
            if self.player.rect.left < 0 :
                self.player.vel.x = 0
                self.player.acc.x = 0
                self.player.pos.x = self.player.image.get_width()/2
            elif self.player.rect.right > WIDTH :
                self.player.vel.x = 0
                self.player.acc.x = 0
                self.player.pos.x = WIDTH - self.player.image.get_width()/2

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
                    if keys[pg.K_SPACE] :
                        self.player.jump_reverse(True)
                if self.player.vel.x < 0 and nbCollideLeft > 0:
                    self.player.vel.x = 0
                    self.player.acc.x = 0
                    self.player.pos.x = hits[ind].rect.right + self.player.image.get_width()/2
                    self.player.slidingR = True
                    if keys[pg.K_SPACE]:
                            self.player.jump_reverse(False)

        if self.player.rect.top > HEIGHT:
            self.player.vel.x = 0
            self.player.acc.x = 0
            self.player.pos.x = self.current_level.x_start
            self.player.pos.y = self.current_level.y_start


        if keys[pg.K_DELETE]:
            self.level = 0
            self.time_elapsed = 0


            self.playing = False
        if keys[pg.K_r]:
            self.player.vel.x = 0
            self.player.acc.x = 0
            self.player.pos.x = self.current_level.x_start
            self.player.pos.y = self.current_level.y_start



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
        self.all_sprites.draw(self.screen)
        if self.freeplay == False:
            self.draw_text("Time : "+str(round(180 - self.time_elapsed/100,1))+'s', 30, WHITE, 90, 20)
            self.draw_text("Score : "+str(self.score), 30, WHITE, 240, 20)
            self.draw_text("Hightscore : "+str(self.hightscore), 30, WHITE, 400, 20)
        else :
            self.draw_text("Speed X : "+str(round(abs(self.player.vel.x),1)), 30, WHITE, 90, 20)
            self.draw_text("Speed Y : "+str(round(abs(self.player.vel.y),1)), 30, WHITE, 270, 20)

        self.screen.blit(self.player.image, self.player.rect)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_level(self) :
        num_ligne = 0
        for line in self.current_level.struct:
            nume_case = 0
            for sprite in line :
                x = nume_case * 8*SIZE_PLAT
                y = num_ligne * 8*SIZE_PLAT
                if sprite == '0':
                    Background(self,x,y,0)
                if sprite == '1':
                    Platform(self,x,y,0)
                if sprite == '2':
                    Platform(self,x,y,19)
                if sprite == '3':
                    Platform(self,x,y,1)
                if sprite == '4':
                    Platform(self,x,y,20)
                if sprite == '5':
                    Platform(self,x,y,2)
                if sprite == '6':
                    Platform(self,x,y,21)
                if sprite == '7':
                    Platform(self,x,y,3)
                if sprite == '8':
                    Platform(self,x,y,22)
                if sprite == '9':
                    Platform(self,x,y,4)
                if sprite == 'a':
                    Platform(self,x,y,23)
                if sprite == 'b':
                    Platform(self,x,y,5)
                if sprite == 'c':
                    Platform(self,x,y,24)
                if sprite == 'd':
                    Platform(self,x,y,6)
                if sprite == 'e':
                    Platform(self,x,y,25)
                if sprite == 'f':
                    Platform(self,x,y,7)
                if sprite == 'g':
                    Platform(self,x,y,26)
                if sprite == 'h':
                    Platform(self,x,y,8)
                if sprite == 'i':
                    Platform(self,x,y,27)
                if sprite == 'j':
                    Platform(self,x,y,9)
                if sprite == 'k':
                    Platform(self,x,y,28)
                if sprite == 'l':
                    Platform(self,x,y,10)
                if sprite == 'm':
                    Platform(self,x,y,29)
                if sprite == 'n':
                    Platform(self,x,y,11)
                if sprite == 'o':
                    Platform(self,x,y,30)
                if sprite == 'p':
                    Platform(self,x,y,12)
                if sprite == 'q':
                    Platform(self,x,y,31)
                if sprite == 'r':
                    Platform(self,x,y,13)
                if sprite == 's':
                    Platform(self,x,y,32)
                if sprite == 't':
                    Platform(self,x,y,14)
                if sprite == 'u':
                    Platform(self,x,y,33)
                if sprite == 'v':
                    Platform(self,x,y,15)
                if sprite == 'w':
                    Platform(self,x,y,34)
                if sprite == 'x':
                    Platform(self,x,y,16)
                if sprite == 'y':
                    Platform(self,x,y,35)
                if sprite == 'z':
                    Platform(self,x,y,17)
                if sprite == 'A':
                    Platform(self,x,y,36)
                if sprite == 'B':
                    Platform(self,x,y,18)
                if sprite == 'C':
                    Platform(self,x,y,37)
                if sprite == 'D':
                    pass
                if sprite == 'E':
                    pass
                if sprite == 'F':
                    pass
                if sprite == 'G':
                    pass
                if sprite == 'H':
                    pass
                if sprite == 'I':
                    pass
                if sprite == 'J':
                    Background(self,x,y,1)
                if sprite == 'K':
                    Background(self,x,y,2)
                if sprite == 'L':
                    Background(self,x,y,3)
                if sprite == 'M':
                    Background(self,x,y,4)
                if sprite == 'N':
                    Background(self,x,y,5)
                if sprite == 'O':
                    Background(self,x,y,6)
                if sprite == 'P':
                    Background(self,x,y,7)
                if sprite == 'Q':
                    Background(self,x,y,8)
                if sprite == 'R':
                    Background(self,x,y,9)
                if sprite == 'S':
                    Background(self,x,y,10)
                if sprite == 'T':
                    Background(self,x,y,11)
                if sprite == 'U':
                    Background(self,x,y,12)
                if sprite == 'V':
                    Background(self,x,y,13)
                if sprite == 'W':
                    Background(self,x,y,14)
                if sprite == 'X':
                    Background(self,x,y,15)
                if sprite == 'Y':
                    Background(self,x,y,16)
                if sprite == 'Z':
                    Background(self,x,y,17)
                if sprite == '!':
                    Background(self,x,y,18)
                if sprite == '"':
                    Background(self,x,y,19)
                if sprite == '#':
                    Background(self,x,y,20)
                if sprite == '$':
                    Background(self,x,y,21)
                if sprite == '%':
                    Background(self,x,y,22)
                if sprite == '+':
                    Background(self,x,y,23)
                if sprite == ',':
                    Background(self,x,y,24)
                if sprite == '-':
                    Background(self,x,y,25)
                if sprite == '.':
                    Background(self,x,y,26)
                if sprite == '/':
                    Background(self,x,y,27)
                if sprite == ':':
                    Background(self,x,y,28)
                if sprite == ';':
                    Background(self,x,y,29)
                if sprite == '(':
                    Background(self,x,y,30)
                if sprite == '<':
                    Background(self,x,y,31)
                if sprite == '=':
                    Background(self,x,y,32)
                if sprite == '>':
                    Background(self,x,y,33)
                if sprite == '?':
                    Background(self,x,y,34)
                if sprite == '@':
                    Background(self,x,y,35)
                if sprite == '&':
                    Background(self,x,y,36)
                if sprite == '`':
                    Background(self,x,y,37)
                if sprite == '{':
                    Background(self,x,y,38)
                if sprite == ')':
                    Background(self,x,y,39)
                if sprite == '|':
                    Background(self,x,y,40)
                if sprite == '[':
                    Lave(self,x,y,0)
                if sprite == '\\':
                    Lave(self,x,y,1)
                if sprite == ']':
                    Lave(self,x,y,2)
                if sprite == '^':
                    Lave(self,x,y,3)
                if sprite == '_':
                    Lave(self,x,y,4)
                if sprite == '*':
                    Background(self, x ,y, 41)
                if sprite == '}':
                    Background(self, x, y, 42)
                if sprite == '~':
                    LevelEnd(self,x,y)
                if sprite == '\'':
                    Ressort(self,x,y,0)

                nume_case += 1
            num_ligne += 1
    def draw_start_screen(self):
        pg.mixer.music.load(path.join(g.sound_dir, 'start_screen_music.ogg'))
        pg.mixer.music.play(loops=-1)
        background = pg.image.load(path.join(self.img_dir, "ecrantitre.png"))
        self.screen.blit(background,(0,0))

        images_button = [self.spritesheet_button.get_image(0,0,290,138),
                  self.spritesheet_button.get_image(0,139,300,132),
                  self.spritesheet_button.get_image(0,385,290,109),
                  self.spritesheet_button.get_image(0,272,287,112)]
        self.screen.blit(images_button[0],(127,180))
        self.screen.blit(images_button[1],(572,180))
        self.screen.blit(images_button[2],(351,396))
        self.screen.blit(images_button[3],(351,567))

        pg.display.flip()
        self.wait_for_click_start()
        self.playing = True


    def draw_score_screen(self):
        background = pg.image.load(path.join(self.img_dir, "ecranfinRIP.png"))
        backgroundGG = pg.image.load(path.join(self.img_dir, "ecranfinYa.png"))
        if self.score > self.hightscore :
            if self.score > self.hightscore:
                self.hightscore = self.score
                with open(path.join(self.dir, HS_FILE), 'w') as f:
                    f.write(str(self.score))

            self.screen.blit(backgroundGG,(0,0))
            self.draw_text(str(self.score), 100, WHITE, 520, 275)
        else:
            self.screen.blit(background,(0,0))
            self.draw_text(str(self.hightscore), 100, WHITE, 520, 250)
            self.draw_text(str(self.score), 100, WHITE, 520, 450)
        self.score = 0


        pg.display.flip()
        self.wait_for_key()

    def draw_option_screen(self):
        background = pg.image.load(path.join(self.img_dir, "ecranoption.png"))
        self.screen.blit(background,(0,0))
        pg.display.flip()
        self.wait_for_click_option()
        self.draw_start_screen()

    def draw_credit_screen(self):
        background = pg.image.load(path.join(self.img_dir, "ecrancredit.png"))
        self.screen.blit(background,(0,0))
        pg.display.flip()
        self.wait_for_click_option()
        self.draw_start_screen()



    def wait_for_click_start(self):
        waiting = True
        event = pg.event.poll()
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pg.mouse.get_pos()
                    if pos[0] > 127 and pos[1] > 180 and pos[0] < 427 and pos[1] < 312:
                        waiting = False
                        pg.mixer.fadeout(500)
                    if pos[0] > 351 and pos[1] > 396 and pos[0] < 641 and pos[1] < 505:
                        self.draw_option_screen()
                    if pos[0] > 351 and pos[1] > 567 and pos[0] < 638 and pos[1] < 679:
                        self.draw_credit_screen()
                    if pos[0] > 572 and pos[1] > 180 and pos[0] < 872 and pos[1] < 312:
                        self.freeplay = True
                        waiting = False
                        pg.mixer.fadeout(500)



    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting =False

    def wait_for_click_option(self):
        waiting = True
        event = pg.event.poll()
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pg.mouse.get_pos()
                    if pos[0] > 16 and pos[1] > 66 and pos[0] < 131 and pos[1] < 117:
                        waiting = False




g = Game()
BD_story = pg.image.load(path.join(g.img_dir, "striprun.png"))
g.screen.blit(BD_story,(0,0))
pg.display.flip()
pg.time.delay(5000)
g.draw_start_screen()
while g.running:
    g.new()
    if g.freeplay == False:
        g.draw_score_screen()

pg.quit()
