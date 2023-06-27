import pygame
from pygame.locals import *
from pygame import mixer  # para poder cargar música en python
import pickle
from os import path #importar path, servirá para comprobar el máximo de archivos data para los niveles

from Buton import Button
from Player import Player
from World1 import World
from Enemy import Enemy
from Platform import Platform
from Lava import Lava
from Coin import Coin
from Exit import Exit


pygame.mixer.pre_init(44100, -16, 2, 512)  # predefinir configuración para el mixer
mixer.init()  # iniciar mixer para sonido
pygame.init()  # iniciar pygame

clock = pygame.time.Clock() #reloj
fps = 60  # número de frames per secon

screen_width = 800  # anchura de la pantalla
screen_height = 800 # altura de la pantalla

screen = pygame.display.set_mode((screen_width, screen_height)) #pantalla
pygame.display.set_caption('Survivor')  # añadir el nombre a la ventana del juego

# definir fuente para texto
font = pygame.font.SysFont('Bauhaus 93', 70)  # definir la fuente para Game Over, Winner y su tamaño
font_score = pygame.font.SysFont('Bauhaus 93', 30)  # definir la fuente para Game Over, Winner y su tamaño

# definir variables del juego
tile_size = 40
game_over = 0  # comenzar con variable game over a 0, significa jugar
main_menu = True  # inicializar con el menú = true, para que se muestre y no inicié directamente el juego
level = 2  # comenzar nivel 0
max_levels = 7  # definir máximo de niveles a 7
score = 0  # empezar con la variable puntuación a 0

# definir colores
white = (255, 255, 255)  # color blanco definido para el texto de las monedas o a necesitar
blue = (0, 0, 255)  # color azul definido para el texto de Game Over, Winner o a necesitar

# cargar imagenes

bg = pygame.image.load('Graficos/Background.jpg')  # cargar imagen fondo pantalla
bg_img = pygame.transform.scale(bg, (800, 800))
restart_img = pygame.image.load('Graficos/Botones/button_restart.png')  # cargar imagen botón reset
start_img = pygame.image.load('Graficos/Botones/button_start.png')  # cargar imagen botón comenzar
exit_img = pygame.image.load('Graficos/Botones/button_exit.png')  # cargar imagen botón exit

# cargar sonidos
pygame.mixer.music.load('Audio/music.wav')  # sonido para el juego de fondo
pygame.mixer.music.play(-1, 0.0, 5000)  # activar sonido juego de fondo con un delay de 5000ms
coin_fx = pygame.mixer.Sound('Audio/coin.wav')  # sonido para coger moneda
coin_fx.set_volume(0.5)  # definir volumen al 50%
jump_fx = pygame.mixer.Sound('Audio/jump.wav')  # sonido para saltar
jump_fx.set_volume(0.5)  # definir volumen al 50%
game_over_fx = pygame.mixer.Sound('Audio/game_over.wav')  # sonido para game over
game_over_fx.set_volume(0.5)  # definir volumen al 50%


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# función resetear nivel
def reset_level(level):
    player.reset(80, screen_height - 120)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()

    # cargar nivel data y cargar el mundo
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    # create dummy coin for showing the score
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)
    return world

player = Player(100, screen_height - 130)  # definir posición inicial del jugador en pantalla

blob_group = pygame.sprite.Group()  # variable grupal enemigos
platform_group = pygame.sprite.Group()  # variable grupal plataformas
lava_group = pygame.sprite.Group()  # variable grupal lava
coin_group = pygame.sprite.Group()  # variable grupal monedas
exit_group = pygame.sprite.Group()  # variable grupal exit

# crear moneda para el contador
score_coin = Coin(tile_size // 2, tile_size // 2)  # crear moneda para el contador de monedas y su tamaño
coin_group.add(score_coin)  # llamar a la imagen moneda

# cargar nivel data y cargar el mundo
if path.exists(f'level{level}_data'):  # función para llamar al próximo nivel si existe
    pickle_in = open(f'level{level}_data', 'rb')  # función para abrir el nivel solicitado
    world_data = pickle.load(pickle_in)
world = World(world_data)

# crear botones
restart_button = Button(screen_width // 2 - 80, screen_height // 2 + 100,
                        restart_img)  # crear botón reset con su tamaño y posición
start_button = Button(screen_width // 2 - 250, screen_height // 2,
                      start_img)  # crear botón empezar con su tamaño y posición
exit_button = Button(screen_width // 2 + 50, screen_height // 2, exit_img)  # crear botón exit con su tamaño y posición

run = True  # para inicializar
while run:  # bucle

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))  # definir donde cargar la imagen del fondo de pantalla

    if main_menu == True:  # comprobar si el menú está true
        if exit_button.draw():  #
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:  # comprobar si game over = 0, lo que significa que no se ha perdido, juego en marcha
            blob_group.update()  # actualizar enemigos
            platform_group.update()  # actualizar plataformas
            # actualizar contador y comprobar si una moneda ha sido cogida
            if pygame.sprite.spritecollide(player, coin_group, True):  # detectar collision con una moneda y elimanarla con true
                score += 1  # aumentar contador +1
                coin_fx.play()  # llamar al sonido de coger moneda
            draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)  # texto para mostrar las monedas en pantalla

        blob_group.draw(screen)  # mostrar enemigos en la pantalla
        platform_group.draw(screen)  # mostrar plataformas en la pantalla
        lava_group.draw(screen)  # mostrar la lava en la pantalla
        coin_group.draw(screen)  # mostrar monedas en la pantalla
        exit_group.draw(screen)  # mostrar puerta en la pantalla

        game_over = player.update(game_over)  # actualizar en caso de game over el jugador

        # comprobar si el jugador ha muerto
        if game_over == -1:  # comprobar si ha habido colisión con alguna muerte
            if restart_button.draw():  # comprobar si el botón restart ha sido pulsado
                world_data = []  # vacir la lista de niveles, es decir antes estaba cargado nivel1 por ejemplo, vaciarlo
                world = reset_level(level)  # resetear nivel
                game_over = 0  # poner game over a 0, por lo tanto volver a permitir jugar
                score = 0  # poner puntuación a 0

        # comprobar si el jugador ha completado el nivel
        if game_over == 1:  # comprobar si game over =1, significa victoria
            # resetear juego y ir al siguiente nivel
            level += 1  # aumentar nivel
            if level <= max_levels:  # comprobar que no se haya llegado al máximo de niveles
                # resetear nivel
                world_data = []  # vacir la lista de niveles, es decir antes estaba cargado nivel1 por ejemplo, vaciarlo
                world = reset_level(level)  # resetear nivel
                game_over = 0  # poner game over a 0, por lo tanto volver a permitir jugar
            else:
                draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140,
                          screen_height // 2)  # dibujar texto has ganado, definiendo la fuente,color tamaño y posición
                if restart_button.draw():  # comprobar si el botón restart ha sido pulsado
                    level = 1  # volver al nivel 1, ya que significaría volver a empezar el juego des de cero
                    # resetear nivel
                    world_data = []  # vacir la lista de niveles, es decir antes estaba cargado nivel1 por ejemplo, vaciarlo
                    world = reset_level(level)  # resetear nivel
                    game_over = 0  # poner game over a 0, por lo tanto volver a permitir jugar
                    score = 0  # poner puntuación a 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # comprobar si se ha pedido salir
            run = False  # parar run

    pygame.display.update()

pygame.quit()  # salir de pygame
