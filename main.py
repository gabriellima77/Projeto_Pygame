from settings import *
import pygame
from pygame.locals import *
import sys

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Font
font = pygame.font.Font("Anton-Regular.ttf", 30)

# Background
background = pygame.image.load("img/background.jpg")

# sprites
path ='img/sprites/'
sprite_idle = (pygame.image.load(path + "idle/adventurer-idle-00.png").convert(), pygame.image.load(path + "idle/adventurer-idle-01.png").convert(), pygame.image.load(path + "idle/adventurer-idle-02.png").convert())
sprite_run_r = (pygame.image.load(path + "run/adventurer-run-00.png").convert(), pygame.image.load(path + "run/adventurer-run-01.png").convert(), pygame.image.load(path + "run/adventurer-run-02.png").convert(),
                pygame.image.load(path + "run/adventurer-run-03.png").convert(), pygame.image.load(path + "run/adventurer-run-04.png").convert(), pygame.image.load(path + "run/adventurer-run-05.png").convert())
sprite_run_l = []
for s in sprite_run_r:
    sprite_run_l.append(pygame.transform.flip(s, True, False))


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = sprite_idle[0].get_size()[0]
        self.height = sprite_idle[0].get_size()[1]
        self.vel = 2.5
        self.left = False
        self.right = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

block_rect = pygame.Rect(50, 0, 50, 50)

def show_text(x, y, text, color, font):
    text_render = font.render(text, True, color)
    screen.blit(text_render, (x, y))


def main_menu():
    while True:
        screen.fill(BLACK)
        game()
        screen.blit(background, (0, 0))
        show_text(293, 33, 'Projeto Teste', BLACK, font)
        show_text(290, 30, 'Projeto Teste', WHITE, font)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(FPS)


def animation(frame):
    if not p.left and not p.right:
        sprite = sprite_idle
    else:
        if p.left:
            sprite = sprite_run_l
        else:
            sprite = sprite_run_r
    sprite_index = frame // 7
    if sprite_index < len(sprite):
        screen.blit(sprite[sprite_index], (p.x, p.y))
        return frame
    else:
        sprite_index = 0
        screen.blit(sprite[sprite_index], (p.x, p.y))
        return sprite_index


p = Player()


def game():
    running = True
    frame = 0
    while running:
        screen.fill(BLACK)
        frame = animation(frame)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and p.x > p.vel:
            p.left = True
            p.x -= p.vel
            p.rect.x = p.x
        else:
            p.left = False
        if keys[pygame.K_RIGHT] and p.x < SIZE[0] - p.width:
            p.right = True
            p.x += p.vel
            p.rect.x = p.x
        else:
            p.right = False
        pygame.display.update()
        clock.tick(FPS)
        frame += 1


main_menu()
