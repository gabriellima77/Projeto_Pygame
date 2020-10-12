from settings import *
import pygame
from pygame.locals import *
import sys
from sprites import *

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)
display = pygame.Surface((SIZEUP[0], SIZEUP[1]))

# Font
font = pygame.font.Font("Anton-Regular.ttf", 30)

# Background
background = pygame.image.load("img/background.jpg")


def show_text(x, y, text, color, font):
    text_render = font.render(text, True, color)
    display.blit(text_render, (x, y))


def main_menu():
    while True:
        screen.fill(BLACK)
        game()
        display.blit(background, (0, 0))
        show_text(293, 33, 'Projeto Teste', BLACK, font)
        show_text(290, 30, 'Projeto Teste', WHITE, font)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
player = Player()
platforms = pygame.sprite.Group()
all_sprites.add(player)


def load_map():
    file = open("map.txt", "r")
    map = file.read()
    i = j = 0
    for cell in map:
        if cell == '\n':
            i += 1
            j = -1
        if cell == '1':
            p = Platforms(j, i)
            all_sprites.add(p)
            platforms.add(p)
        j += 1
    file.close()


def collision_test():
    hit_list = []
    tiles = []
    for p in platforms:
        tiles.append(p.rect)
    for tile in tiles:
        if player.rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move():
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    hit_list = collision_test()
    print(player.rect.bottom)
    for tile in hit_list:
        if player.rect.right > tile.left  and player.rect.right  < tile.right and player.rect.bottom >= tile.bottom:
                player.rect.right = tile.left - 24
                player.velocity.x = 0
                player.position.x = player.rect.right
                collision_types['right'] = True
        elif player.rect.left <= tile.right and player.rect.left > tile.left and player.rect.bottom >= tile.bottom:
                player.rect.left = tile.right + 25
                player.velocity.x = 0
                player.position.x = player.rect.left
                collision_types['left'] = True
        elif player.rect.bottom > tile.top and player.rect.bottom < tile.bottom:
                player.rect.bottom = tile.top + 1
                player.velocity.y = 0
                player.position.y = player.rect.bottom
                player.jumping = False
        elif player.velocity.y < 0:
            player.rect.top = tile.bottom + 1
            collision_types["top"] = True
    return collision_types
load_map()


def game():
    running = True
    while running:
        hits = pygame.sprite.spritecollide(player, platforms, False)
        move()
        '''if player.rect.right > SIZE[1] / 4:
            player.position.x += abs(player.velocity.x)
            for plat in platforms:
                plat.rect.x += abs(player.velocity.x)
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if (event.key == K_w or event.key == K_UP) and not player.jumping:
                    player.jump()
        all_sprites.update()
        display.fill(BLACK)
        all_sprites.draw(display)
        for sprite in platforms:
            if player.rect.colliderect(sprite.rect):
                pygame.draw.rect(display, (0, 255, 0), sprite.rect)
        screen.blit(pygame.transform.scale(display, SIZE), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


main_menu()
