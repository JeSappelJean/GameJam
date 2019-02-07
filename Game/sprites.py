import pygame as pg
from settings import *
vec = pg.math.Vector2


class Spritesheet:
    #charger et coisir le bon sprites "parsing"
    def __init__(self, filename,size):
        self.spritesheet_car = pg.image.load(filename).convert_alpha()
        self.size = size

    def get_image(self, x, y, w, h):
        image = pg.Surface((w, h))
        image.blit(self.spritesheet_car, (0, 0), (x, y, w, h))
        image = pg.transform.scale(image, (w*self.size, h*self.size))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x ,y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet_car.get_image(9, 12, 15, 20)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x ,  y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumpCount = 0
        self.walking = False
        self.jumping = False
        self.dashing = False
        self.slidingR = False
        self.slidingL = False
        self.gravity = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()

    def load_images(self):
        self.standing_frames = [self.game.spritesheet_car.get_image(200, 108, 17, 20),
                                self.game.spritesheet_car.get_image(234, 108, 17, 20)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet_car.get_image(9, 12, 15, 20),
                              self.game.spritesheet_car.get_image(41, 11, 15, 20),
                              self.game.spritesheet_car.get_image(72, 12, 16, 20),
                              self.game.spritesheet_car.get_image(104, 11, 17, 20)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame_r_up =[self.game.spritesheet_car.get_image(168, 11, 16, 20)]
        self.jump_frame_l_up = []
        for frame in self.jump_frame_r_up:
            frame.set_colorkey(BLACK)
            self.jump_frame_l_up.append(pg.transform.flip(frame, True, False))

        self.jump_frame_r_down = [self.game.spritesheet_car.get_image(201, 11, 15, 20)]
        self.jump_frame_l_down = []
        for frame in self.jump_frame_r_down:
            frame.set_colorkey(BLACK)
            self.jump_frame_l_down.append(pg.transform.flip(frame, True, False))

        self.dash_frames_r = [self.game.spritesheet_car.get_image(136, 109, 17, 19)]
        self.dash_frames_l = []
        for frame in self.dash_frames_r:
            frame.set_colorkey(BLACK)
            self.dash_frames_l.append(pg.transform.flip(frame, True, False))

        self.wall_slide_r = [self.game.spritesheet_car.get_image(490, 108, 16, 20)]
        self.wall_slide_l = []
        for frame in self.wall_slide_r:
            frame.set_colorkey(BLACK)
            self.wall_slide_l.append(pg.transform.flip(frame, True, False))

    def jump(self):
        #self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        #self.rect.x -=1


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
        if self.gravity == True:
            self.acc = vec(0,0)
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                    self.acc.x -= PLAYER_ACC_GRAV
            if keys[pg.K_RIGHT]:
                self.acc.x += PLAYER_ACC_GRAV
            if keys[pg.K_UP]:
                    self.acc.y -= PLAYER_ACC_GRAV
            if keys[pg.K_DOWN]:
                self.acc.y += PLAYER_ACC_GRAV

            self.vel += self.acc
            if abs(self.vel.x) < 0.1:
                self.vel.x = 0
            if abs(self.vel.y) < 0.1:
                self.vel.y = 0

            if self.vel.x > 10:
                self.vel.x = 10
            elif self.vel.x < -10:
                self.vel.x = -10

            if self.vel.y > 10:
                self.vel.y = 10
            elif self.vel.y < -10:
                self.vel.y = -10

            self.pos += self.vel  + 0.5 * self.acc

            self.rect.midbottom = self.pos

        else :
            self.animate()
            self.acc = vec(0,PLAYER_GRAV)
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                    self.acc.x -= PLAYER_ACC
            if keys[pg.K_RIGHT]:
                self.acc.x += PLAYER_ACC
            if keys[pg.K_LEFT] and keys[pg.K_q] and self.game.time_elapsed > PLAYER_DASH_TIME:
                self.acc.x -= PLAYER_ACC*10
                self.dashing = True
                self.game.time_elapsed = 0
            if keys[pg.K_RIGHT] and keys[pg.K_q] and self.game.time_elapsed > PLAYER_DASH_TIME:
                self.acc.x += PLAYER_ACC*10
                self.dashing = True
                self.game.time_elapsed = 0


            #appliquer la friction
            self.acc.x += self.vel.x * PLAYER_FRICTION

            #équation de mouvement
            self.vel += self.acc
            if abs(self.vel.x) < 0.1:
                self.vel.x = 0

            self.pos += self.vel  + 0.5 * self.acc

            self.rect.midbottom = self.pos


    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.x !=0 :
            self.walking = True
        else:
            self.walking = False

        if self.vel.x !=0 or self.vel.y ==0:
            self.slidingR = False
            self.slidingL = False

        if abs(self.vel.x) < 10:
            self.dashing = False


        if self.vel.y !=0 :
            self.jumping = True
        else:
            self.jumping = False

        if self.walking:
            if self.dashing:
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.dash_frames_r)
                    bottom = self.rect.bottom
                    if self.vel.x > 0:
                        self.image = self.dash_frames_r[self.current_frame]
                    else :
                        self.image = self.dash_frames_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            elif not self.jumping:
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                    bottom = self.rect.bottom
                    if self.vel.x > 0:
                        self.image = self.walk_frames_r[self.current_frame]
                    else :
                        self.image = self.walk_frames_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom



        if self.jumping:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frame_r_up)
                bottom = self.rect.bottom
                if self.vel.x > 0 and self.vel.y > 0:
                    self.image = self.jump_frame_r_down[self.current_frame]
                elif self.vel.x > 0 and self.vel.y < 0:
                    self.image = self.jump_frame_r_up[self.current_frame]
                elif self.vel.x < 0 and self.vel.y > 0:
                    self.image = self.jump_frame_l_down[self.current_frame]
                elif self.vel.x < 0 and self.vel.y < 0:
                    self.image = self.jump_frame_l_up[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 600:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.slidingR or self.slidingL :
            if now - self.last_update > 20:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.wall_slide_r)
                bottom = self.rect.bottom
                if self.slidingR:
                    self.image = self.wall_slide_r[self.current_frame]
                else :
                    self.image = self.wall_slide_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x , y, img):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images_l = [self.game.spritesheet_plat.get_image(8,8,8,8),
                  self.game.spritesheet_plat.get_image(0,8,8,8),
                  self.game.spritesheet_plat.get_image(0,16,8,8),
                  self.game.spritesheet_plat.get_image(0,24,8,8),
                  self.game.spritesheet_plat.get_image(8,24,8,8),
                  self.game.spritesheet_plat.get_image(16,8,8,8),
                  self.game.spritesheet_plat.get_image(16,16,8,8),
                  self.game.spritesheet_plat.get_image(32,32,8,8),
                  self.game.spritesheet_plat.get_image(24,32,8,8),
                  self.game.spritesheet_plat.get_image(24,40,8,8),
                  self.game.spritesheet_plat.get_image(24,48,8,8),
                  self.game.spritesheet_plat.get_image(32,48,8,8),
                  self.game.spritesheet_plat.get_image(40,32,8,8),
                  self.game.spritesheet_plat.get_image(32,8,8,8),
                  self.game.spritesheet_plat.get_image(24,8,8,8),
                  self.game.spritesheet_plat.get_image(24,16,8,8),
                  self.game.spritesheet_plat.get_image(24,24,8,8),
                  self.game.spritesheet_plat.get_image(32,24,8,8),
                  self.game.spritesheet_plat.get_image(40,8,8,8)]
        images_r = []
        for frame in images_l:
            images_r.append(pg.transform.flip(frame, True, False))
        images = images_l + images_r
        self.image = images[img]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Background(pg.sprite.Sprite):
    def __init__(self, game, x , y, img):
        self.groups = game.all_sprites, game.background
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet_plat.get_image(0,0,8,8),
                  self.game.spritesheet_plat.get_image(56,24,8,8),
                  self.game.spritesheet_plat.get_image(8,40,8,8),
                  self.game.spritesheet_plat.get_image(40,40,8,8),
                  pg.transform.flip(self.game.spritesheet_plat.get_image(40,40,8,8), True, False),
                  self.game.spritesheet_plat.get_image(48,32,8,8),
                  self.game.spritesheet_plat.get_image(0,48,8,8),
                  self.game.spritesheet_plat.get_image(40,48,8,8),
                  self.game.spritesheet_plat.get_image(56,32,8,8),
                  self.game.spritesheet_plat.get_image(8,48,8,8),
                  self.game.spritesheet_plat.get_image(32,40,8,8),
                  self.game.spritesheet_plat.get_image(40,80,8,8),
                  self.game.spritesheet_plat.get_image(48,80,8,8),
                  self.game.spritesheet_plat.get_image(56,80,8,8),
                  self.game.spritesheet_plat.get_image(16,24,8,8),
                  self.game.spritesheet_plat.get_image(56,0,8,8),
                  self.game.spritesheet_plat.get_image(48,0,8,8),
                  self.game.spritesheet_plat.get_image(40,0,8,8),
                  self.game.spritesheet_plat.get_image(32,0,8,8),
                  self.game.spritesheet_plat.get_image(24,0,8,8),
                  self.game.spritesheet_plat.get_image(16,0,8,8),
                  self.game.spritesheet_plat.get_image(8,0,8,8),
                  self.game.spritesheet_plat.get_image(8,16,8,8),
                  self.game.spritesheet_plat.get_image(32,56,8,8),
                  self.game.spritesheet_plat.get_image(0,64,8,8),
                  self.game.spritesheet_plat.get_image(8,64,8,8),
                  self.game.spritesheet_plat.get_image(16,64,8,8),
                  self.game.spritesheet_plat.get_image(24,72,8,8),
                  self.game.spritesheet_plat.get_image(0,88,8,8),
                  self.game.spritesheet_plat.get_image(24,64,8,8),
                  pg.transform.flip(self.game.spritesheet_plat.get_image(24,64,8,8), True, False),
                  self.game.spritesheet_plat.get_image(0,72,8,8),
                  self.game.spritesheet_plat.get_image(8,72,8,8),
                  self.game.spritesheet_plat.get_image(16,72,8,8),
                  self.game.spritesheet_plat.get_image(32,72,8,8),
                  self.game.spritesheet_plat.get_image(8,88,8,8),
                  pg.transform.flip(self.game.spritesheet_plat.get_image(8,88,8,8), True, False),
                  self.game.spritesheet_plat.get_image(16,88,8,8),
                  self.game.spritesheet_plat.get_image(24,88,8,8),
                  pg.transform.flip(self.game.spritesheet_plat.get_image(24,88,8,8), True, False),
                  self.game.spritesheet_plat.get_image(32,88,8,8),
                  pg.transform.flip(self.game.spritesheet_plat.get_image(40,80,8,8), True, False),
                  self.game.spritesheet_plat.get_image(32,64,8,8)]

        self.image = images[img]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lave(pg.sprite.Sprite):
    def __init__(self, game, x , y, img):
        self.groups = game.all_sprites, game.lave
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet_plat.get_image(0,80,8,8),
                 self.game.spritesheet_plat.get_image(8,80,8,8),
                 self.game.spritesheet_plat.get_image(16,80,8,8),
                 self.game.spritesheet_plat.get_image(24,80,8,8),
                 self.game.spritesheet_plat.get_image(32,80,8,8)]

        self.image = images[img]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Niveau:
    def __init__(self, filename):
        self.fichier = filename
        self.struct = 0
        self.x_start = 0
        self.y_start = 0
        self.generate()

    def generate(self):
        with open(self.fichier, "r") as fichier:
            structure_niveau = []
            for ligne in fichier:
                ligne_niveau = []
                for sprite in ligne:
                    if sprite != '\n':
                        ligne_niveau.append(sprite)
                structure_niveau.append(ligne_niveau)
            self.struct = structure_niveau

            pos = ''.join(structure_niveau[-1]).split(',')
            if len(pos) > 1:
                self.x_start = int(pos[1])
                self.y_start = int(pos[2])
