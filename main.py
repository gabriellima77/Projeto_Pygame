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


def get_collision(player, tile):
    hit_rect_list = []
    for i in tile:
        if player.rect.colliderect(i.rect):
            hit_rect_list.append(i.rect)
    return hit_rect_list


def collision(player, tiles):
    hits = get_collision(player, tiles)
    for hit in hits:
        if player.rect.left < hit.right and (player.rect.left > hit.left and hit.bottom < player.rect.bottom):
            player.rect.left = hit.right
            player.velocity.x = 0
            player.position.x = player.rect.left
        elif player.rect.right > hit.left and (player.rect.right < hit.right and hit.bottom < player.rect.bottom):
            player.rect.right = hit.left
            player.velocity.x = 0
            player.position.x = player.rect.right - 49
        elif player.rect.bottom > hit.top and player.rect.bottom < hit.bottom:
            player.rect.bottom = hit.top + 1
            player.position.y = player.rect.top
            player.velocity.y = 0
            player.jumping = False
        elif player.rect.top + 5 < hit.bottom and player.velocity.y < 0:
            player.velocity.y = 0


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
        collision(player, platforms)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if (event.key == K_w or event.key == K_UP) and not player.jumping:
                    player.jump()
        all_sprites.update()
        camera.update(player)
        display.fill(BLACK)
        for sprite in all_sprites:
            display.blit(sprite.image, camera.apply(sprite))
        screen.blit(pygame.transform.scale(display, SIZE), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


main_menu()
