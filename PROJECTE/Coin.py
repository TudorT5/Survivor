import pygame
from pygame.sprite import Sprite

class Coin(Sprite):  # definición de la clase lava
    def __init__(self, x, y):  # inicializar
        Sprite.__init__(self)
        img = pygame.image.load('Graficos/coin.png')  # cargar imagen de moneda
        self.image = pygame.transform.scale(img, (35, 35))  # escalar la imagen
        self.rect = self.image.get_rect()  # crear rectangulo
        self.rect.center = (x, y)  # definir los corners
