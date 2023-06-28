import pygame
from Constantes import *

class Platform(pygame.sprite.Sprite):  # definición de la clase plataforma
    def __init__(self, x, y, move_x, move_y):  # inicializar
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Graficos/Plat_1.png')  # cargar imagen de la plataforma
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))  # escalar la imagen
        self.rect = self.image.get_rect()  # crear rectangulo a la imagen plataforma
        self.rect.x = x  # definir corner x
        self.rect.y = y  # definir corner y
        self.move_counter = 0  # definir el contador para poder moverlas en 0
        self.move_direction = 1  # definir el movimiento de las plataformas
        self.move_x = move_x  # definir movimiento para plataforma en x
        self.move_y = move_y  # definir movimiento para plataforma en y

    def update(
            self):  # actualizar el movimiento de las plataformas, ir incrementandolo en 1 hasta llegar a 50, para invertir el sentido restando -1, añadir que se ha multiplicado por self.move_x, para así ahorrarnos de crear otra clase extra para el movimiento en x e y, ya que al multiplicar por (0,1), en caso de tener la x*self_movedirection, el resultado será 0 y por lo tanto no permitira que la plataforma se mueva en y, y viceversa
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1

