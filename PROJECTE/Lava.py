import pygame
from pygame.sprite import Sprite
from Constantes import *


class Lava(Sprite):  # definición de la clase lava
    def __init__(self, x, y):  # inicializar
        Sprite.__init__(self)
        img = pygame.image.load('Graficos/Pinchos.png')  # cargar imagen de lava
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))  # escalar la imagen
        self.rect = self.image.get_rect()  # crear rectangulo
        self.rect.x = x  # definir corner x
        self.rect.y = y  # definir corner y