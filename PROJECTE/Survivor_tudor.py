import pygame
from pygame.locals import *
from pygame import mixer  # para poder cargar música en python
import pickle
from os import path #importar path, servirá para comprobar el máximo de archivos data para los niveles
from Constantes import * #importar del archivo constantes
from Sprites import * #importar del archivo sprites
from Button import Button #importar clase button del archivo button
from Coin import Coin #importar clase coin del archivo coin
from World import World #importar clase world del archivo world



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
bg_img = pygame.transform.scale(bg, (800, 800)) #escalar la imagen del fondo
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
exit_fx = pygame.mixer.Sound('Audio/exit.wav')  # sonido para saltar
exit_fx.set_volume(0.5)  # definir volumen al 50%
game_over_fx = pygame.mixer.Sound('Audio/game_over.wav')  # sonido para game over
game_over_fx.set_volume(0.5)  # definir volumen al 50%



def draw_text(text, font, text_col, x, y): #dibujar el texto
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# función resetear nivel
def reset_level(level):
    player.reset(80, screen_height - 120)
    ghost_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()

    # cargar nivel data y cargar el mundo
    if path.exists(f'Levels/level{level}_data'):
        pickle_in = open(f'Levels/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data, screen)
    # crear moneda para el marcador
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
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:  # comprobar flecha izquierda y derecha para que el personaje no se mueva
                self.counter = 0
                self.index = 0
                if self.direction == 1:  # comprobar direccion para la imagen del personaje
                    self.image = self.images_right[self.index]  # cambiar imagen del personaje mirando hacia la derecha
                if self.direction == -1:  # comprobar direccion para la imagen del personaje
                    self.image = self.images_left[self.index]  # cambiar imagen del personaje mirando hacia la derecha

            # animación, aumentando el contador de la lista self.index y irlo actualizando
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
            if pygame.sprite.spritecollide(self, ghost_group, False):  # buscar colisión y no eliminar el objeto (False)
                game_over = -1  # pasar a game over -1, significa has perdido y el juego se para
                game_over_fx.play()  # llamar al sonido de salto

            # comprobar colisión con lava
            if pygame.sprite.spritecollide(self, lava_group, False):  # buscar colisión y no eliminar el objeto (False)
                game_over = -1  # pasar a game over -1, significa has perdido y el juego se para
                game_over_fx.play()  # llamar al sonido de salto

            # comprobar colisión con la puerta
            if pygame.sprite.spritecollide(self, exit_group, False):  # buscar colisión y no eliminar el objeto (False)
                game_over = 1  # pasar a game over 1, significa has ganado o avanzas de nivel

            # comprobar colisión con la plataforma móvil
            for platform in platform_group:
                # comprobar colisión en x
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):  # buscar colisión
                    dx = 0  # diferencia de x igual a 0
                # comprobar colisión en y
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):  # buscar colisión
                    # comprobar colisión saltando con plataforma móvil y cabeza
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # comprobar colisión caiendo a plataforma móvil
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # moverse con la plataforma móvil
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # actualizar cordenadas del jugador
            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1: #mostrar texto en pantalla "GAME OVER"
            self.image = self.dead_image
            draw_text('GAME OVER!', font, red, (screen_width // 2) - 250, (screen_height // 2) - 100)
            if self.rect.y > 200:
                self.rect.y -= 5

        # ddibujar jugador en pantalla
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y): #mostrar imagen del personaje dirección derecha y izquierda y de muerte
        self.images_right = [] #lista en blanco
        self.images_left = [] #lista en blanco
        self.index = 0 #para escoger la variable de la lista
        self.counter = 0 # contador para controlar la velocidad de animación
        for num in range(1, 5): #para seleccionar en caso de querer mas imagenes con el mismo nombre
            img_right = pygame.image.load(f'Graficos/Flork/Flork_{num}.png') #cargar imagen del personaje derecha
            img_right = pygame.transform.scale(img_right, (32, 64)) #escalar imagen
            img_left = pygame.transform.flip(img_right, True, False) #invertir imagen para así ahorrarnos crear la imagen hacia la derecha
            self.images_right.append(img_right) #mandar a la lista el valor de image right
            self.images_left.append(img_left) #mandar a la lista el valor de image left
        dead = pygame.image.load('Graficos/Flork/Flork_dead.png') #cargar imagen del personaje muerto
        self.dead_image = pygame.transform.scale(dead, (32, 64)) #escalar imagen
        self.image = self.images_right[self.index]  #cargar la imagen al empezar que es sin moverse, la primera de todas
        self.rect = self.image.get_rect() #crear rectangulo
        self.rect.x = x #definir rectangulo en x
        self.rect.y = y #definir rectangulo en y
        self.width = self.image.get_width() #coger anchura
        self.height = self.image.get_height() #coger altura
        self.vel_y = 0 #velocidad en y
        self.jumped = False #salto false
        self.direction = 0 #dirección 0 (parado sin hacer nada)
        self.in_air = True #salto


player = Player(100, screen_height - 130)  # definir posición inicial del jugador en pantalla


# crear moneda para el contador
score_coin = Coin(tile_size // 2, tile_size // 2)  # crear moneda para el contador de monedas y su tamaño
coin_group.add(score_coin)  # llamar a la imagen moneda


# cargar nivel data y cargar el mundo
if path.exists(f'Levels/level{level}_data'):  # función para llamar al próximo nivel si existe
    pickle_in = open(f'Levels/level{level}_data', 'rb')  # función para abrir el nivel solicitado
    world_data = pickle.load(pickle_in) #cargar en world data el valor del pickle
world = World(world_data, screen) #mostrar en pantalla world con el valor de data cargado


# crear botones
restart_button = Button(screen_width // 2 - 80, screen_height // 2 + 100, restart_img, screen)  # crear botón reset con su tamaño y posición
start_button = Button(screen_width // 2 - 250, screen_height // 2, start_img, screen)  # crear botón empezar con su tamaño y posición
exit_button = Button(screen_width // 2 + 50, screen_height // 2, exit_img, screen)  # crear botón exit con su tamaño y posición



run = True  # para inicializar
while run:  # bucle

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))  # definir donde cargar la imagen del fondo de pantalla

    if main_menu == True:  # comprobar si el menú está true y posteriormente comprobar si alguno de los dos botones han sido clicados y por lo tanto ejecutar la opción de parar el run del juego, o quitar el menú y jugar
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:  # comprobar si game over = 0, lo que significa que no se ha perdido, juego en marcha
            ghost_group.update()  # actualizar enemigos
            platform_group.update()  # actualizar plataformas
            # actualizar contador y comprobar si una moneda ha sido cogida
            if pygame.sprite.spritecollide(player, coin_group, True):  # detectar collision con una moneda y elimanarla con true
                score += 1  # aumentar contador +1
                coin_fx.play()  # llamar al sonido de coger moneda
            draw_text('  ' + str(score), font_score, white, tile_size - 10, 10)  # texto para mostrar las monedas en pantalla

        ghost_group.draw(screen)  # mostrar enemigos en la pantalla
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

    pygame.display.update() #actualizar

pygame.quit()  # salir de pygame



#world_data = [
#[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
#[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
#[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
#[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
#[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
#[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
#[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
#[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
#[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
#[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
#[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#]