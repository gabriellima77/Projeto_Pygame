from player_actions import move
import pygame


class Tile:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 10, 10)

    def change_place(self, x, y):
        self.rect.x = x
        self.rect.y = y


class MapTest:
    def __init__(self):
        self.width = 100
        self.height = 100


class PlayerTest:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 10, 10)   ## x, y, width, height
        self.movement = [0, 0]
        self.momentum = 0

    def move(self, x, y, speed, jumping, falling):
        self.rect.x = x
        self.rect.y = y
        self.movement[0] = speed
        if(jumping):
            self.movement[1] = -4


p = PlayerTest()
tile_map = MapTest()
tile = [Tile()]


def test_collision_right():
    p.move(-4, 0, 5, False, False)
    assert move(p, tile, tile_map)["Right"] == True


def test_collision_left():
    p.move(4, 0, -5, False, False)
    assert move(p, tile, tile_map)["Left"] == True


def test_collision_top():
    p.move(0, 0, 0, True, False)
    tile[0].change_place(0, -10)
    assert move(p, tile, tile_map)["Top"] == True
