import sys
import os
import pygame


# Agregar la ruta raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from menu import MainMenu

class Game:
    def __init__(self):
        pygame.init()
        self.screen_w = 400
        self.screen_h = 500
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Prueba del Menú")
        self.running = True
        self.playing = False

    def run(self):
        main_menu = MainMenu(self)
        main_menu.display_menu()

if __name__ == "__main__":
    game = Game()
    game.run()
