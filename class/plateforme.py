import pygame
from pygame.locals import *

class Joueur :

    speed_x = 0
    speed_y = 0
    niveau = 0

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
    
