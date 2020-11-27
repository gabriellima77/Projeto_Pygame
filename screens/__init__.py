from player_actions import move
from screens.screens_settings import *
from eventsKey import *
from exceptions import *


def information():
    running = True
    background = pygame.image.load("assets/img/Help.png")

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


def winner():
    try:
        screen.fill(BLACK)
        show_text(SIZE[0]/2, SIZE[1]/2, "YOU WIN", WHITE, font_generics)
        pygame.display.update()
        pygame.mixer.music.load('assets/sound/end.mp3')
        pygame.mixer.music.play(-1)
        running = True
        global phase, death
        phase = 1
        death = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                        pygame.mixer.music.load('assets/sound/open.mp3')
                        pygame.mixer.music.play(-1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        running = False
                        pygame.mixer.music.load('assets/sound/open.mp3')
                        pygame.mixer.music.play(-1)
    except pygame.error as err:
        pygame_error(err)

    except FileNotFoundError as err:
        filenotfound_error(err)


def game():
    try:
        player = end = 0
        running = True
        change_map()
        global phase, death
        pygame.mixer.music.load('assets/sound/phase.mp3')
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
            if player.rect.colliderect(end):
                phase += 1
                death += player.death
                running = False
                menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                eventChange(event,player)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        information()
                    if event.key == pygame.K_RETURN:
                        player.move_r = False
                        player.move_l = False
                        running = False
                        death += player.death
                        phase += 1
                        menu()

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
            player.rect, collisions = move(player.rect, player.movement, platforms, player, tile_map)
            if collisions['Bottom']:
                player.jumping = False
                player.falling = False
                player.momentum = 0
                player.jump_time = 0
            else:
                player.jump_time += 1
            if player.momentum > 1 and not player.jumping:
                player.falling = True
            camera.update(player)
            display.fill((85, 180,   255))
            display.blit(map_img, camera.apply_rect(map_rect))
            for sprite in all_sprites:
                display.blit(sprite.image, camera.apply(sprite))
            screen.blit(pygame.transform.scale(display, SIZE), (0, 0))
            show_text(SIZE[0] - 150, 10, "Deaths: " + str(death+player.death), WHITE, font_generics)
            pygame.display.update()

            clock.tick(FPS)
    except pygame.error as err:
        pygame_error(err)

    except FileNotFoundError as err:
        filenotfound_error(err)


def menu():
    if phase == 1:
        print(f"Phase:{phase}")
        game()
    elif phase == 2:
        print(f"Phase:{phase}")
        game()
    elif phase == 3:
        print(f"Phase:{phase}")
        game()
    elif phase == 4:
        winner()
    else:
        pygame.quit()
        sys.exit()


def change_map():
    global tile_map
    global map_rect
    global map_img
    try:
        tile_map = TiledMap("map/tile_map" + str(phase) + ".tmx")
        map_img = tile_map.make_map()
        map_rect = map_img.get_rect()
    except FileNotFoundError as err:
        filenotfound_error(err)


def show_text(x, y, text, text_color, text_font):
    text_surface = text_font.render(text, True, text_color)
    screen.blit(text_surface, (int(x), int(y)))
