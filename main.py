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


def get_collision(rect, tile):
    hit_rect_list = []
    for i in tile:
        if rect.colliderect(i.rect):
            hit_rect_list.append(i.rect)
    return hit_rect_list


def move(rect, movement, tiles):
    collision_type = {'Top': False, 'Right': False, 'Bottom': False, 'Left': False}
    rect.x += movement[0]
    hits = get_collision(rect, tiles)
    for tile in hits:
        if movement[0] > 0:
            collision_type['Right'] = True
            rect.right = tile.left
        if movement[0] < 0:
            collision_type['Left'] = True
            rect.left = tile.right
    rect.y += movement[1]
    hits = get_collision(rect, tiles)
    for tile in hits:
        if movement[1] > 0:
            collision_type['Bottom'] = True
            rect.bottom = tile.top
        if movement[1] < 0:
            collision_type['Top'] = True
            rect.top = tile.bottom
    return rect, collision_type


def show_text(x, y, text, text_color, text_font):
    text_render = text_font.render(text, True, text_color)
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


def load_map(sprites, platform):
    file = open("map.txt", "r")
    m = file.read()
    i = j = 0
    for cell in m:
        if cell == '\n':
            i += 1
            j = -1
        if cell == '1':
            p = Platforms(j, i)
            sprites.add(p)
            platform.add(p)
        j += 1
    file.close()
    return i*32, j*32


def game():
    running = True
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    player = Player(platforms)
    all_sprites.add(player)
    map_size = load_map(all_sprites, platforms)
    camera = Camera(map_size[0], map_size[1])
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if (event.key == K_w or event.key == K_UP) and not player.jumping:
                    player.jumping = True
                    if player.jump_time < 6:
                        player.momentum = -5
                if event.key == K_RIGHT or event.key == K_d:
                    player.move_r = True
                if event.key == K_LEFT or event.key == K_a:
                    player.move_l = True
            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    player.move_r = False
                if event.key == K_LEFT or event.key == K_a:
                    player.move_l = False
        all_sprites.update()
        player.movement = [0, 0]
        if player.move_r:
            player.movement[0] += 4
        if player.move_l:
            player.movement[0] -= 4
        player.movement[1] += player.momentum
        player.momentum += GRAV
        if player.momentum > 7:
            player.momentum = 7
        player.rect, collisions = move(player.rect, player.movement, platforms)
        if collisions['Bottom']:
            player.jumping = False
            player.momentum = 0
            player.jump_time = 0
        else:
            player.jump_time += 1
        camera.update(player)
        display.fill(BLACK)
        for sprite in all_sprites:
            display.blit(sprite.image, camera.apply(sprite))
        screen.blit(pygame.transform.scale(display, SIZE), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


main_menu()
