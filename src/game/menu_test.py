import sys
import os
import pygame


# Agregar la ruta raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from menu import MainMenu

class Game:
    def __init__(self):
        pygame.init()
        self.screen_w = 600
        self.screen_h = 500
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Prueba del Menú")
        self.running = True
        self.playing = False
        self.contagion_enabled = True  # Estado inicial de la enfermedad
        # Reglas iniciales del juego
        self.rules = {
            "contagion_prob_near": 0.3,  # Probabilidad de contagio cercano
            "contagion_prob_distant": 0.1,  # Probabilidad de contagio a distancia
            "mortality_prob": 0.05,  # Probabilidad de que una celda infectada muera
            "recovery_prob": 0.2,  # Probabilidad de recuperación
        }

    def run(self):
        main_menu = MainMenu(self)
        main_menu.display_menu()

if __name__ == "__main__":
    game = Game()
    game.run()
