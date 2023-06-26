SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 552

FPS = 60
# Colores:

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255,100,150)
TEAL = (100,255,255)
ORANGE = (230,190,40)
GREEN = (0, 255, 0)

PROTA = 0

for row in data:
    col_count = 0
    for tile in row:
        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
        img_rect = img.get_rect()
        img_rect.x = col_count * tile_size
        img_rect.y = row_count * tile_size
        tile = (img, img_rect)
        if tile == 1:
            self.tile_list.append(tile)
        elif tile == 2:
            self.tile_list.append(tile)
        else:
            col_count += 1
    row_count += 1

