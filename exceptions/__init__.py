import pygame
from py_speak import speak_text
import sys

def pygame_error(err):
    pygame.mixer.music.pause()
    speak_text("Um erro no pai game aconteceu.")
    print(err)
    pygame.quit()
    sys.exit()

def filenotfound_error(err):
    pygame.mixer.music.pause()
    speak_text("Um erro aconteceu. Um diretorio não foi encontrado ")
    print(err)
    pygame.quit()
    sys.exit()
