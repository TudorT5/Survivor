import pygame
tile_size = 40
class Coin(pygame.sprite.Sprite):  # definición de la clase lava
    def __init__(self, x, y):  # inicializar
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Graficos/estrella.png')  # cargar imagen de moneda
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))  # escalar la imagen
        self.rect = self.image.get_rect()  # crear rectangulo
        self.rect.center = (x, y)  # definir los corners

