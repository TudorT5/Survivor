import pygame
from pygame.locals import *
from pygame import mixer  # para poder cargar música en python
import pickle
from os import path #importar path, servirá para comprobar el máximo de archivos data para los niveles


pygame.mixer.pre_init(44100, -16, 2, 512)  # predefinir configuración para el mixer
mixer.init()  # iniciar mixer para sonido
pygame.init()  # iniciar pygame

clock = pygame.time.Clock()
fps = 60  # número de frames per secon

screen_width = 800  # anchura de la pantalla
screen_height = 800 # altura de la pantalla

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Survivor')  # añadir el nombre a la ventana del juego

# define font
font = pygame.font.SysFont('Bauhaus 93', 70)  # definir la fuente para Game Over, Winner y su tamaño
font_score = pygame.font.SysFont('Bauhaus 93', 30)  # definir la fuente para Game Over, Winner y su tamaño

# define game variables
tile_size = 40
game_over = 0  # comenzar con variable game over a 0, significa jugar
main_menu = True  # inicializar con el menú = true, para que se muestre y no inicié directamente el juego
level = 2  # comenzar nivel 0
max_levels = 7  # definir máximo de niveles a 7
score = 0  # empezar con la variable puntuación a 0

# define colours
white = (255, 255, 255)  # color blanco definido para el texto de las monedas o a necesitar
blue = (0, 0, 255)  # color azul definido para el texto de Game Over, Winner o a necesitar

# load images

bg = pygame.image.load('Graficos/Background.jpg')  # cargar imagen fondo pantalla
bg_img = pygame.transform.scale(bg, (800, 800))
restart_img = pygame.image.load('Graficos/Botones/button_restart.png')  # cargar imagen botón reset
start_img = pygame.image.load('Graficos/Botones/button_start.png')  # cargar imagen botón comenzar
exit_img = pygame.image.load('Graficos/Botones/button_exit.png')  # cargar imagen botón exit

# load sounds
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


# function to reset level
def reset_level(level):
    player.reset(80, screen_height - 120)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()

    # load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    # create dummy coin for showing the score
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)
    return world


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()  # detectar tecla pulsada
            if key[
                pygame.K_SPACE] and self.jumped == False and self.in_air == False:  # detectar tecla espacio y condiciones para no poder saltar infinitas veces
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

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            self.in_air = True
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):  # buscar colisión y no eliminar el objeto (False)
                game_over = -1  # pasar a game over -1, significa has perdido y el juego se para
                game_over_fx.play()  # llamar al sonido de salto

            # check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):  # buscar colisión y no eliminar el objeto (False)
                game_over = -1  # pasar a game over -1, significa has perdido y el juego se para
                game_over_fx.play()  # llamar al sonido de salto

            # check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):  # buscar colisión y no eliminar el objeto (False)
                game_over = 1  # pasar a game over 1, significa has ganado o avanzas de nivel

            # check for collision with platforms
            for platform in platform_group:
                # collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):  # buscar colisión
                    dx = 0  # diferencia de x igual a 0
                # collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):  # buscar colisión
                    # check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font, blue, (screen_width // 2) - 180, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player onto screen
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


class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        dirt_img = pygame.image.load('Graficos/Plat_1.png')  # cargar imagen suelo
        grass_img = pygame.image.load('Graficos/Plat_1.png')  # cargar imagen hierba

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  # comprobar si vale 1 para generar la imagen
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))  # escalar la imagen al tamaño pedido
                    img_rect = img.get_rect()  # crear rectangulo
                    img_rect.x = col_count * tile_size  #
                    img_rect.y = row_count * tile_size  #
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:  # comprobar si vale 2 para generar la imagen
                    img = pygame.transform.scale(grass_img,
                                                 (tile_size, tile_size))  # escalar la imagen al tamaño pedido
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:  # comprobar si vale 3 para generar la imagen
                    blob = Enemy(col_count * tile_size,
                                 row_count * tile_size - 10)  # escalar la imagen al tamaño pedido y ajustarla en pantalla
                    blob_group.add(blob)  # añadir la imagen al grupo
                if tile == 4:  # comprobar si vale 4 para generar la imagen
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1,
                                        0)  # escalar la imagen al tamaño pedido y ajustarla en pantalla, el 1,0 es para el movimiento en x
                    platform_group.add(platform)  # añadir la imagen al grupo
                if tile == 5:  # comprobar si vale 5 para generar la imagen
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0,
                                        1)  # escalar la imagen al tamaño pedido y ajustarla en pantalla, el 0,1 es para el movimiento en y
                    platform_group.add(platform)  # añadir la imagen al grupo
                if tile == 6:  # comprobar si vale 6 para generar la imagen
                    lava = Lava(col_count * tile_size, row_count * tile_size + (
                                tile_size // 2))  # escalar la imagen al tamaño pedido y ajustarla en pantalla
                    lava_group.add(lava)  # añadir la imagen al grupo
                if tile == 7:  # comprobar si vale 7 para generar la imagen
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (
                                tile_size // 2))  # escalar la imagen al tamaño pedido y ajustarla en pantalla
                    coin_group.add(coin)  # añadir la imagen al grupo
                if tile == 8:  # comprobar si vale 8 para generar la imagen
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))  # escalar la imagen al tamaño pedido y ajustarla en pantalla
                    exit_group.add(exit)
                col_count += 1  # añadir a col_count 1
            row_count += 1  # añadir a row_count 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


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


class Lava(pygame.sprite.Sprite):  # definición de la clase lava
    def __init__(self, x, y):  # inicializar
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Graficos/Pinchos.png')  # cargar imagen de lava
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))  # escalar la imagen
        self.rect = self.image.get_rect()  # crear rectangulo
        self.rect.x = x  # definir corner x
        self.rect.y = y  # definir corner y


class Coin(pygame.sprite.Sprite):  # definición de la clase lava
    def __init__(self, x, y):  # inicializar
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Graficos/estrella.png')  # cargar imagen de moneda
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))  # escalar la imagen
        self.rect = self.image.get_rect()  # crear rectangulo
        self.rect.center = (x, y)  # definir los corners


class Exit(pygame.sprite.Sprite):  # definición de la clase lava
    def __init__(self, x, y):  # inicializar
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Graficos/Puerta.png')  # cargar imagen del botón exit
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))  # escalar la imagen
        self.rect = self.image.get_rect()  # crear rectangulo
        self.rect.x = x  # definir corner x
        self.rect.y = y  # definir corner y


player = Player(100, screen_height - 130)  # definir posición inicial del jugador en pantalla

blob_group = pygame.sprite.Group()  # variable grupal enemigos
platform_group = pygame.sprite.Group()  # variable grupal plataformas
lava_group = pygame.sprite.Group()  # variable grupal lava
coin_group = pygame.sprite.Group()  # variable grupal monedas
exit_group = pygame.sprite.Group()  # variable grupal exit

# create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)  # crear moneda para el contador de monedas y su tamaño
coin_group.add(score_coin)  # llamar a la imagen moneda

# load in level data and create world
if path.exists(f'level{level}_data'):  # función para llamar al próximo nivel si existe
    pickle_in = open(f'level{level}_data', 'rb')  # función para abrir el nivel solicitado
    world_data = pickle.load(pickle_in)
world = World(world_data)

# create buttons
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
            # update score
            # check if a coin has been collected
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

        # if player has died
        if game_over == -1:  # comprobar si ha habido colisión con alguna muerte
            if restart_button.draw():  # comprobar si el botón restart ha sido pulsado
                world_data = []  # vacir la lista de niveles, es decir antes estaba cargado nivel1 por ejemplo, vaciarlo
                world = reset_level(level)  # resetear nivel
                game_over = 0  # poner game over a 0, por lo tanto volver a permitir jugar
                score = 0  # poner puntuación a 0

        # if player has completed the level
        if game_over == 1:  # comprobar si game over =1, significa victoria
            # reset game and go to next level
            level += 1  # aumentar nivel
            if level <= max_levels:  # comprobar que no se haya llegado al máximo de niveles
                # reset level
                world_data = []  # vacir la lista de niveles, es decir antes estaba cargado nivel1 por ejemplo, vaciarlo
                world = reset_level(level)  # resetear nivel
                game_over = 0  # poner game over a 0, por lo tanto volver a permitir jugar
            else:
                draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140,
                          screen_height // 2)  # dibujar texto has ganado, definiendo la fuente,color tamaño y posición
                if restart_button.draw():  # comprobar si el botón restart ha sido pulsado
                    level = 1  # volver al nivel 1, ya que significaría volver a empezar el juego des de cero
                    # reset level
                    world_data = []  # vacir la lista de niveles, es decir antes estaba cargado nivel1 por ejemplo, vaciarlo
                    world = reset_level(level)  # resetear nivel
                    game_over = 0  # poner game over a 0, por lo tanto volver a permitir jugar
                    score = 0  # poner puntuación a 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # comprobar si se ha pedido salir
            run = False  # parar run

    pygame.display.update()

pygame.quit()  # salir de pygame