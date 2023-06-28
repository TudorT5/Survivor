import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

#Ventana juego
tile_size = 30
cols = 20
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * cols) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


#Cargar imagenes

bg_img = pygame.image.load('Graficos/Background.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
plat_img = pygame.image.load('Graficos/Plat_1.png')
ghost_img = pygame.image.load('Graficos/Fantasma.png')
platform_x_img = pygame.image.load('Graficos/Plat_1.png')
platform_y_img = pygame.image.load('Graficos/Plat_1.png')
lava_img = pygame.image.load('Graficos/Pinchos.png')
coin_img = pygame.image.load('Graficos/coin.png')
exit_img = pygame.image.load('Graficos/Puerta.png')
save_img = pygame.image.load('Graficos/Botones/button_start.png')
load_img = pygame.image.load('Graficos/Botones/button_exit.png')


#Definir variables juego
clicked = False
level = 1

#Definir Colores
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#Crear lista vacia
world_data = []
for row in range(20):
	r = [0] * 20
	world_data.append(r)

#Crear limites
for tile in range(0, 20):
	world_data[19][tile] = 2
	world_data[0][tile] = 1
	world_data[tile][0] = 1
	world_data[tile][19] = 1

#Crear texto en la pantalla
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for c in range(21):
		#Lineas verticales
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
		#Lineas horizontales
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1 or 2:
					#Plataforma
					img = pygame.transform.scale(plat_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					#Enemigos
					img = pygame.transform.scale(ghost_img, (tile_size, int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
				if world_data[row][col] == 4:
					#Plataforma horizontal
					img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5:
					#plataforma vertical
					img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 6:
					#lava
					img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				if world_data[row][col] == 7:
					#moneda
					img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 8:
					#exit
					img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
					screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))



class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#posicion del raton
		pos = pygame.mouse.get_pos()

		#posicion del ratón y click del ratón
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#Boton mostrar
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

#Botones guardar y cargar
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)

#Bucle principal
run = True
while run:

	clock.tick(fps)

	#fondo
	screen.fill(green)
	screen.blit(bg_img, (0, 0))


	#Cargar y guardar nivel
	if save_button.draw():
		#guardar nivel
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#cargar en level data
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)


	#mostrar rejilla
	draw_grid()
	draw_world()


	#mostrar nivel actual
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

	#Evento
	for event in pygame.event.get():
		#Salir del juego
		if event.type == pygame.QUIT:
			run = False
		#clicar para cmabiar imagen
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#comprobar que estas dentro del cuadrado de la rejilla
			if x < 20 and y < 20:
				#actualizar valor del cuadrado de la rejilla
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 8:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 8
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#cambiar de nivel con las flechas arriba y abajo
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#actualizar pantalla
	pygame.display.update()

pygame.quit()