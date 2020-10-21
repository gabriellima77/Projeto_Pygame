from settings import *
import pygame
from pygame.locals import *
import sys
from sprites import *

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()


screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)
display = pygame.Surface((SIZEUP[0], SIZEUP[1]))

# Font
font_button = pygame.font.Font("SansitaSwashed-VariableFont_wght.ttf", 23)

# Background
background = pygame.image.load("img/Gaeron.png")

phase = 1
# Map's variables
tile_map = TiledMap("map/tile_map"+str(phase)+".tmx")
map_img = tile_map.make_map()
map_rect = map_img.get_rect()


def information():
    running = True
    background = pygame.image.load("img/Help.png")

    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.update()


def change_map():
    global tile_map
    global map_rect
    global map_img

    tile_map = TiledMap("map/tile_map"+str(phase)+".tmx")
    map_img = tile_map.make_map()
    map_rect = map_img.get_rect()


def get_collision(rect, tile):
    hit_rect_list = []
    for i in tile:
        if rect.colliderect(i.rect):
            hit_rect_list.append(i.rect)
    return hit_rect_list


def fall(player):
    if player.rect.y > tile_map.height:
        for tile_object in tile_map.tmxdata.objects:
            if tile_object.name == "player":
                player.rect.x = int(tile_object.x)
                player.rect.y = int(tile_object.y)
                player.death += 1


def move(rect, movement, tiles, player):
    collision_type = {'Top': False, 'Right': False, 'Bottom': False, 'Left': False}
    fall(player)
    if tile_map.width > rect.x >= 0:
        rect.x += movement[0]
        if rect.x < 0:
            rect.x = 0
        if rect.x > tile_map.width - 32:
            rect.x = tile_map.width - 32
    hits = get_collision(rect, tiles)
    for tile in hits:
        if movement[0] > 0:
            collision_type['Right'] = True
            rect.right = tile.left
        if movement[0] < 0:
            collision_type['Left'] = True
            rect.left = tile.right
    rect.y += round(movement[1])
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
    text_surface = text_font.render(text, True, text_color)
    screen.blit(text_surface, (x, y))


def main_menu():
    x = 0
    acc = 2
    click = False
    player2 = Player(200, 50)
    button_play = Button(260, 300, 'img/UI/ui1.png')
    button_info = Button(280, 350, 'img/UI/ui2.png')
    pygame.mixer.music.load('open.mp3')
    pygame.mixer.music.play(-1)
    while True:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        mx, my = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if button_play.circle_rect.collidepoint((mx, my)) or button_play.txt_rect.collidepoint((mx, my)):
            if click:
                pygame.mixer.music.stop()
                menu()
        if button_info.circle_rect.collidepoint((mx, my)) or button_info.txt_rect.collidepoint((mx, my)):
            if click:
                information()
        screen.blit(button_play.img_circle, (button_play.circle_rect.x, button_play.circle_rect.y))
        screen.blit(button_play.img_txt, (button_play.txt_rect.x, button_play.txt_rect.y))
        screen.blit(button_info.img_circle, (button_info.circle_rect.x, button_info.circle_rect.y))
        screen.blit(button_info.img_txt, (button_info.txt_rect.x, button_info.txt_rect.y))
        player2.update()
        show_text(button_play.txt_rect.center[0] - 10, button_play.txt_rect.center[1] - 10, 'Play', BLACK, font_button)
        show_text(button_info.txt_rect.center[0] - 10, button_info.txt_rect.center[1] - 10, 'Info', BLACK, font_button)
        if acc > 0:
            player2.move_l = False
            player2.move_r = True
        else:
            player2.move_r = False
            player2.move_l = True
        screen.blit(pygame.transform.scale(player2.image, (32, 30)), (x, 420))
        x += acc
        if x > SIZE[0] - 32 or x < 0:
            acc *= -1
        if pygame.mixer.music.get_pos() == 206:
            pygame.mixer.music.get_pos()
            pygame.mixer.music.load('open.mp3')
            pygame.mixer.music.play()

        pygame.display.update()
        clock.tick(FPS)


def menu():
    if phase == 1:
        print("Phase:1")
        game()
    elif phase == 2:
        print("Phase:2")
        game()
    elif phase == 3:
        print("Phase:3")
        game()

    else:
        pygame.quit()
        sys.exit()


def game():
    player = end = 0
    running = True
    change_map()
    global phase
    pygame.mixer.music.load('phase.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_pos(10)  # 10
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    for tile_object in tile_map.tmxdata.objects:
        if tile_object.name == 'player':
            player = Player(tile_object.x, tile_object.y)
        if tile_object.name == 'platform':
            Platforms(platforms, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        if tile_object.name == 'end':
            end = pygame.Rect(int(tile_object.x), int(tile_object.y), int(tile_object.width), int(tile_object.height))
        else:
            end = pygame.Rect(3168, 867, 32, 32)
    all_sprites.add(player)
    camera = Camera(tile_map.width, tile_map.height)
    while running:
        print(player.rect.x, player.rect.y)
        if player.rect.colliderect(end):
            phase += 1
            running = False
            menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and not player.jumping:
                    player.jumping = True
                    if player.jump_time < 6:
                        player.momentum = -5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move_r = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move_l = True
                if event.key == pygame.K_ESCAPE:
                    information()
                if event.key == pygame.K_RETURN and phase == 0:
                    player.move_r = False
                    player.move_l = False
                    phase = 1
                    running = False
                elif event.key == pygame.K_RETURN and phase == 1:
                    phase = 2
                    running = False
                    menu()
                elif event.key == pygame.K_RETURN and phase == 2:
                    phase = 3
                    running = False
                    menu()
                elif event.key == pygame.K_RETURN and phase == 3:
                    phase = 1
                    running = False
                    pygame.mixer.music.load('open.mp3')
                    pygame.mixer.music.play(-1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move_r = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
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
        player.rect, collisions = move(player.rect, player.movement, platforms, player)
        if collisions['Bottom']:
            player.jumping = False
            player.momentum = 0
            player.jump_time = 0
        else:
            player.jump_time += 1
        camera.update(player)
        display.fill((85, 180, 255))
        display.blit(map_img, camera.apply_rect(map_rect))
        for sprite in all_sprites:
            display.blit(sprite.image, camera.apply(sprite))
        screen.blit(pygame.transform.scale(display, SIZE), (0, 0))
        show_text(SIZE[0] - 150, 10, "Deaths: " + str(player.death), WHITE, font_button)
        pygame.display.update()

        clock.tick(FPS)


main_menu()
