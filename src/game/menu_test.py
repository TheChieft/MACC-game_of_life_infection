import sys
import os
import pygame
from menu import MainMenu
from src.utils.constants import CONTAGION_ENABLED, CONTAGION_PROB_NEAR, CONTAGION_PROB_DISTANT, MORTALITY_PROB, RECOVERY_PROB

class Game:
    def __init__(self):
        pygame.init()
        self.screen_w = 600
        self.screen_h = 500
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Prueba del Menú")
        self.running = True
        self.playing = False
        self.rules = {
            "contagion_enabled": CONTAGION_ENABLED,
            "contagion_prob_near": CONTAGION_PROB_NEAR,
            "contagion_prob_distant": CONTAGION_PROB_DISTANT,
            "mortality_prob": MORTALITY_PROB,
            "recovery_prob": RECOVERY_PROB,
        }

    def run(self):
        main_menu = MainMenu(self)
        main_menu.display_menu()


if __name__ == "__main__":
    game = Game()
    game.run()
