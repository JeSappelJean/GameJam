
#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *

#Initialisation de la bibliothèque Pygame
import pygame
from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((640, 480))

#Chargement et collage du fond
fond = pygame.image.load("../img/map.jpg").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso = pygame.image.load("../img/perso.png").convert_alpha()
position_perso = perso.get_rect()
fenetre.blit(perso, position_perso)

#Rafraîchissement de l'écran
pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
pygame.key.set_repeat(400,30)
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                position_perso = position_perso.move(0,5)
            elif event.key == K_RIGHT:
                position_perso = position_perso.move(5,0)
            elif event.key == K_UP:
                position_perso = position_perso.move(0,-5)
            elif event.key == K_LEFT:
                position_perso = position_perso.move(-5,0)
            elif event
    fenetre.blit(fond,(0,0))
    fenetre.blit(perso, position_perso)
    pygame.display.flip()
