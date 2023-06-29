import pygame
from pygame.sprite import Sprite
from Constantes import *

class Exit(Sprite):  # definición de la clase lava
    def __init__(self, x, y):  # inicializar
        Sprite.__init__(self)
        img = pygame.image.load('Graficos/Puerta.png')  # cargar imagen del botón exit
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))  # escalar la imagen
        self.rect = self.image.get_rect()  # crear rectangulo
        self.rect.x = x  # definir corner x
        self.rect.y = y  # definir corner y