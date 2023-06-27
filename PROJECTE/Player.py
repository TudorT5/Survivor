import pygame
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
            draw_text('GAME OVER!', font, blue, (screen_width // 2) - 180, screen_height // 2)
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


