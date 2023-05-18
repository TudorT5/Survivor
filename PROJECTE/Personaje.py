import pygame
from pygame.locals import *
from Constantes import *

class Personaje():
    def __init__(self, x, y):
        img = pygame.image.load("Graficos/Flork/Flork_1.png").convert()
        self.imagen = pygame.transform.scale(img, (36, 21.6))
        self.name = PROTA
        self.alive = True


    def move(self):
        pass

    def die(self):
        self.alive = False


