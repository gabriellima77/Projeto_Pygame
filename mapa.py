from sprites import TiledMap
from pygame_settings import *

def change_map(phase):
	print(phase)
    global tile_map
    global map_rect
    global map_img

    tile_map = TiledMap("map/tile_map"+str(phase)+".tmx")
    map_img = tile_map.make_map()
    map_rect = map_img.get_rect()
