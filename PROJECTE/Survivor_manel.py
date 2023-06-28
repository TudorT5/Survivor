import pygame
from pygame.locals import *
from pygame import mixer  # para poder cargar música en python
import pickle
from os import path #importar path, servirá para comprobar el máximo de archivos data para los niveles
from Constantes import *
from Sprites import *
from Button import Button
from Coin import Coin
from World import World



pygame.mixer.pre_init(44100, -16, 2, 512)  # predefinir configuración para el mixer
mixer.init()  # iniciar mixer para sonido
pygame.init()  # iniciar pygame
clock = pygame.time.Clock() #reloj

screen = pygame.display.set_mode((screen_width, screen_height)) #pantalla
pygame.display.set_caption('Survivor')  # añadir el nombre a la ventana del juego

font = pygame.font.SysFont('Roboto', 120)  # definir la fuente para Game Over, Winner y su tamaño
font_score = pygame.font.SysFont('Roboto', 40)  # definir la fuente para Game Over, Winner y su tamaño

# cargar imagenes

bg = pygame.image.load('Graficos/Background.jpg')  # cargar imagen fondo pantalla
bg_img = pygame.transform.scale(bg, (800, 800))
restart_img = pygame.image.load('Graficos/Botones/button_restart.png')  # cargar imagen botón reset
start_img = pygame.image.load('Graficos/Botones/button_start.png')  # cargar imagen botón comenzar
exit_img = pygame.image.load('Graficos/Botones/button_exit.png')  # cargar imagen botón exit
img_jump = pygame.image.load('Graficos/Flork/Flork_jump.png')
img_jump = pygame.transform.scale(img_jump, (32, 64))


# cargar sonidos
pygame.mixer.music.load('Audio/music.wav')  # sonido para el juego de fondo
pygame.mixer.music.play(-1, 0.0, 5000)  # activar sonido juego de fondo con un delay de 5000ms
coin_fx = pygame.mixer.Sound('Audio/coin.wav')  # sonido para coger moneda
coin_fx.set_volume(0.5)  # definir volumen al 50%
jump_fx = pygame.mixer.Sound('Audio/jump.wav')  # sonido para saltar
jump_fx.set_volume(0.5)  # definir volumen al 50%
exit_fx = pygame.mixer.Sound('Audio/exit.wav')  # sonido para saltar
exit_fx.set_volume(0.5)  # definir volumen al 50%
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
    if path.exists(f'Levels/level{level}_data'):
        pickle_in = open(f'Levels/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data, screen)
    # create dummy coin for showing the score
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)
    return world


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            # comprobar tecla pulsada
            key = pygame.key.get_pressed()  # detectar tecla pulsada
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:  # detectar tecla espacio y condiciones para no poder saltar infinitas veces
                jump_fx.play()  # llamar al sonido de salto
                self.vel_y = -14  # velocidad del salto
                self.jumped = True  # permitir salto
            if key[pygame.K_SPACE] == False:  # comprobar si espacio esta siendo pulsado
                self.jumped = False  # no permitir salto
            if key[pygame.K_LEFT]:  # comprobar flecha izquierda si es pulsada
                dx -= 4  # diferencia de x para evitar colision con plataforma
                self.counter += 1  # aumentar el contador
                self.direction = -1  # sentido de movimiento negativo (izquierda)
            if key[pygame.K_RIGHT]:  # comprobar flecha derecha esta siendo pulsada
                dx += 4  # diferencia de x para evitar colision
                self.counter += 1  # aumentar el contador
                self.direction = 1  # sentido de movimiento negativo (izquierda)
            if key[pygame.K_LEFT] == False and key[
                pygame.K_RIGHT] == False:  # comprobar flecha izquierda y derecha para que el personaje no se mueva
                self.counter = 0
                self.index = 0
                if self.direction == 1:  # comprobar direccion para la imagen del personaje
                    self.image = self.images_right[self.index]  # cambiar imagen del personaje mirando hacia la derecha
                if self.direction == -1:  # comprobar direccion para la imagen del personaje
                    self.image = self.images_left[self.index]  # cambiar imagen del personaje mirando hacia la derecha

            # animación
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # gravedad
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # comprobar colisión
            self.in_air = True
            for tile in world.tile_list:
                # comprobar colisión en x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # comprobar colisión en y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # comprobar colisión saltando con plataforma y cabeza
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # comprobar colisión caiendo a plataforma
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # comprobar colisión con enemigos
            if pygame.sprite.spritecollide(self, blob_group, False):  # buscar colisión y no eliminar el objeto (False)
                game_over = -1  # pasar a game over -1, significa has perdido y el juego se para
                game_over_fx.play()  # llamar al sonido de salto

            # comprobar colisión con lava
            if pygame.sprite.spritecollide(self, lava_group, False):  # buscar colisión y no eliminar el objeto (False)
                game_over = -1  # pasar a game over -1, significa has perdido y el juego se para
                game_over_fx.play()  # llamar al sonido de salto

            # comprobar colisión con la puerta
            if pygame.sprite.spritecollide(self, exit_group, False):  # buscar colisión y no eliminar el objeto (False)
                game_over = 1  # pasar a game over 1, significa has ganado o avanzas de nivel

            # comprobar colisión con la plataforma
            for platform in platform_group:
                # comprobar colisión en x
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):  # buscar colisión
                    dx = 0  # diferencia de x igual a 0
                # comprobar colisión en y
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):  # buscar colisión
                    # comprobar colisión saltando con plataforma y cabeza
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # comprobar colisión caiendo a plataforma
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # moverse con la plataforma
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # actualizar cordenadas del jugador
            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font, red, (screen_width // 2) - 250, (screen_height // 2) - 100)
            if self.rect.y > 200:
                self.rect.y -= 5

        # ddibujar jugador en pantalla
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load('Graficos/Flork/Flork_1.png')
            img_right = pygame.transform.scale(img_right, (32, 64))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        dead = pygame.image.load('Graficos/Flork/Flork_dead.png')
        self.dead_image = pygame.transform.scale(dead, (32, 64))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

player = Player(100, screen_height - 130)  # definir posición inicial del jugador en pantalla


# crear moneda para el contador
score_coin = Coin(tile_size // 2, tile_size // 2)  # crear moneda para el contador de monedas y su tamaño
coin_group.add(score_coin)  # llamar a la imagen moneda


# cargar nivel data y cargar el mundo
if path.exists(f'Levels/level{level}_data'):  # función para llamar al próximo nivel si existe
    pickle_in = open(f'Levels/level{level}_data', 'rb')  # función para abrir el nivel solicitado
    world_data = pickle.load(pickle_in)
world = World(world_data, screen)


# crear botones
restart_button = Button(screen_width // 2 - 80, screen_height // 2 + 100, restart_img, screen)  # crear botón reset con su tamaño y posición
start_button = Button(screen_width // 2 - 250, screen_height // 2, start_img, screen)  # crear botón empezar con su tamaño y posición
exit_button = Button(screen_width // 2 + 50, screen_height // 2, exit_img, screen)  # crear botón exit con su tamaño y posición


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
            draw_text('  ' + str(score), font_score, white, tile_size - 10, 10)  # texto para mostrar las monedas en pantalla

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
            exit_fx.play()
            if level <= max_levels:  # comprobar que no se haya llegado al máximo de niveles
                # resetear nivel
                world_data = []  # vacir la lista de niveles, es decir antes estaba cargado nivel1 por ejemplo, vaciarlo
                world = reset_level(level)  # resetear nivel
                game_over = 0  # poner game over a 0, por lo tanto volver a permitir jugar
            else:
                draw_text('YOU WIN!', font, blue, (screen_width // 2) - 170, (screen_height // 2) - 100)  # dibujar texto has ganado, definiendo la fuente,color tamaño y posición
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