from sprites import *
pygame.init()
from screens import *


def main_menu():
    x = 42
    acc = 2
    player2 = Player(200, 50)
    button_play = Button(260, 300, 'img/UI/ui1.png')
    button_info = Button(280, 350, 'img/UI/ui2.png')
    pygame.mixer.music.load('sound/open.mp3')
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
        show_text(button_play.txt_rect.center[0] - 28, button_play.txt_rect.center[1] - 16, 'Play', BLACK, font_button)
        show_text(button_info.txt_rect.center[0] - 28, button_info.txt_rect.center[1] - 16, 'Info', BLACK, font_button)
        if acc > 0:
            player2.move_l = False
            player2.move_r = True
        else:
            player2.move_r = False
            player2.move_l = True
        screen.blit(pygame.transform.scale(player2.image, (32, 30)), (x, 420))
        x += acc
        if x > SIZE[0] - 40 or x < 40:
            acc *= -1
             
        if pygame.mixer.music.get_pos() == 206:
            pygame.mixer.music.get_pos()
            pygame.mixer.music.load('sound/open.mp3')
            pygame.mixer.music.play()

        pygame.display.update()
        clock.tick(FPS)


main_menu()
