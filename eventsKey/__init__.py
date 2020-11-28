from settings import *


def eventChange(event, player):
    if event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_w or event.key == pygame.K_UP) and not player.jumping:
            player.jumping = True
            player.current_frame = 0
            if player.jump_time < 6:
                player.momentum = -5

        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            player.move_r = True
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            player.move_l = True
    else:
        if eventkeyUp(event) == 1:
            player.move_r = False
        elif eventkeyUp(event) == -1:
            player.move_l = False


def eventkeyUp(event):
    #1
    if event.type == pygame.KEYUP:  # 2
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # 4
            return 1
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:  # 5
            return -1
        else:  # 6
            return 0
    else:  # 3
        return 0
