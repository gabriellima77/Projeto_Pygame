from sprites import *
from exceptions import *


try:
    pygame.mixer.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(TITLE)
    display = pygame.Surface((SIZEUP[0], SIZEUP[1]))

    # Font
    font_button = pygame.font.Font("assets/text_font/SansitaSwashed-VariableFont_wght.ttf", 23)
    font_generics = pygame.font.Font("assets/text_font/Monotype_Gerhilt.ttf", 23)
    phase = 1
    death = 0

    # Background
    background = pygame.image.load("assets/img/Gaeron.png")

    # Map's variables
    tile_map = TiledMap("map/tile_map"+str(phase)+".tmx")
    map_img = tile_map.make_map()
    map_rect = map_img.get_rect()

except pygame.error as err:
    pygame_error(err)

except FileNotFoundError as err:
    filenotfound_error(err)

