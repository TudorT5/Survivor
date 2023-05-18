import pygame, sys
from pygame.locals import *
from Constantes import *



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Survivor")
    fondo = pygame.image.load("Graficos/Background.jpg").convert()
    prota = pygame.image.load("Graficos/Flork/Flork_1.png").convert()
    prota = pygame.transform.scale(prota, (36, 21.6))
    prota_x = 200
    prota_y = 200
    screen.blit(fondo, (0, 0))
    screen.blit(prota, (prota_x, prota_y))
    clock = pygame.time.Clock()

    while True:



        for event in pygame.event.get():
            # Salir del juego
            if event.type == pygame.QUIT:
                sys.exit()

            # Controles
            if event.type == pygame.K:
                if event.key == pygame.K_LEFT:
                    prota_x = prota_x - 2
                elif event.key == pygame.K_RIGHT:
                    prota_x = prota_x + 2

        screen.blit(fondo, (0, 0))
        screen.blit(prota, (prota_x, prota_y))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()




