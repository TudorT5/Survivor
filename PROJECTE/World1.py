import pygame
from pygame.locals import *

tile_size = 40
from Buton import Button
from Player import Player
from Enemy import Enemy
from Platform import Platform
from Lava import Lava
from Coin import Coin
from Exit import Exit

player = Player(100, screen_height - 130)  # definir posición inicial del jugador en pantalla

blob_group = pygame.sprite.Group()  # variable grupal enemigos
platform_group = pygame.sprite.Group()  # variable grupal plataformas
lava_group = pygame.sprite.Group()  # variable grupal lava
coin_group = pygame.sprite.Group()  # variable grupal monedas
exit_group = pygame.sprite.Group()  # variable grupal exit


screen = pygame.display.set_mode((screen_width, screen_height)) #pantalla
pygame.display.set_caption('Survivor')  # añadir el nombre a la ventana del juego

screen_height = 800 # altura de la pantalla
class World():
    def __init__(self, data):
        self.tile_list = []

        # cargar imagenes
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

