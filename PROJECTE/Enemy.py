import pygame
class Enemy(pygame.sprite.Sprite):  # definir clase enemigos
    def __init__(self, x, y):  # inicializar
        pygame.sprite.Sprite.__init__(self)
        imblob = pygame.image.load('Graficos/Fantasma.png')  # cargar imagen enemigos
        self.image = pygame.transform.scale(imblob, (30, 50))
        self.rect = self.image.get_rect()  # crear rectangulo para los enemigos
        self.rect.x = x  # definir corner x
        self.rect.y = y  # definir corner y
        self.move_direction = 1  # definir el movimiento de los enemigos
        self.move_counter = 0  # definir el contador para poder moverlos en 0

    def update(
            self):  # actualizar el movimiento de los enemigos, ir incrementandolo en 1 hasta llegar a 50, para invertir el sentido restando -1
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1

