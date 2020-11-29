import pytest
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
        self.rect = pygame.Rect(0, 0, 10, 10)   ## (x, y, width, height)
        self.movement = [0, 0]
        self.momentum = 0

    def move(self, x, y, speed, jumping, falling):
        self.rect.x = x
        self.rect.y = y
        self.movement[0] = speed
        if jumping and (not falling):
            self.movement[1] = -5
        elif falling:
            self.movement[1] = 5


p = PlayerTest()
tile_map = MapTest()
tile = [Tile(), Tile()]


# No movement
def test_no_movement_collision():
    count = 0
    collision = move(p, tile, tile_map)
    for key in collision:
        if collision[key]:
            count += 1
    assert count == 0


# No collision
def test_no_collision():
    p.move(0, 0, 5, True, False)
    tile[0].change_place(50, 50)
    tile[1].change_place(60, 60)
    count = 0
    collision = move(p, tile, tile_map)
    for key in collision:
        if collision[key]:
            count += 1
    assert count == 0


# Collision with just one tile
def test_collision_right():
    p.move(0, 0, 5, False, False)
    tile[0].change_place(0, 0)
    assert move(p, tile, tile_map)["Right"] == True


def test_collision_left():
    p.move(4, 0, -5, False, False)
    tile[0].change_place(0, 0)
    assert move(p, tile, tile_map)["Left"] == True


def test_collision_top():
    p.move(0, 0, 0, True, False)
    tile[0].change_place(0, -9)
    assert move(p, tile, tile_map)["Top"] is True


def test_collision_bottom():
    p.move(0, 0, 0, False, True)
    tile[0].change_place(0, 5)
    assert move(p, tile, tile_map)["Bottom"] is True


# Collision with two tiles
def test_collision_right_bottom():
    count = 0
    p.move(0, 0, 5, False, True)
    tile[0].change_place(5, 0)
    tile[1].change_place(-9, 5)
    collision = move(p, tile, tile_map)
    for key in collision:
        if collision[key] is True and (key == 'Bottom' or key == 'Right'):
            count += 1
    assert count == 2


def test_collision_right_top():
    count = 0
    p.move(0, 0, 5, True, False)
    tile[0].change_place(5, 0)
    tile[1].change_place(-9, -9)
    collision = move(p, tile, tile_map)
    for key in collision:
        if collision[key] is True and (key == 'Top' or key == 'Right'):
            count += 1
    assert count == 2


def test_collision_left_bottom():
    count = 0
    p.move(0, 0, -5, False, True)
    tile[1].change_place(0, 5)
    collision = move(p, tile, tile_map)
    for key in collision:
        if collision[key] is True and (key == 'Bottom' or key == 'Left'):
            count += 1
    assert count == 2


def test_collision_left_top():
    count = 0
    p.move(0, 0, -5, True, False)
    tile[1].change_place(0, -9)
    collision = move(p, tile, tile_map)
    for key in collision:
        if collision[key] is True and (key == 'Top' or key == 'Left'):
            count += 1
    assert count == 2
