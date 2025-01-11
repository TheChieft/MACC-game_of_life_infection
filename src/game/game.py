import pygame
import numpy as np
from src.utils.constants import *

class Game:
    def __init__(self, screen_width, screen_height, cell_size, rules):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.rules = rules
        self.running = True
        self.paused = False

        # Inicializar Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game of Life Infection")

        # Crear el tablero
        self.cols = self.screen_width // self.cell_size
        self.rows = self.screen_height // self.cell_size
        self.grid = np.zeros((self.rows, self.cols), dtype=int)

        # Estados: 0 = muerta, 1 = viva, 2 = infectada, 3 = recuperada
        self.populate_grid()

    def populate_grid(self):
        """Inicializa el tablero con celdas vivas y muertas aleatoriamente."""
        self.grid = np.random.choice([0, 1], size=(self.rows, self.cols), p=[0.85, 0.15])

    def handle_events(self):
        """Gestiona los eventos del juego, como teclado y ratón."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pausar el juego
                    self.paused = not self.paused
                elif event.key == pygame.K_r:  # Reiniciar el tablero
                    self.populate_grid()

    def update_grid(self):
        """Actualiza el tablero según las reglas del Juego de la Vida y las reglas de contagio."""
        if self.paused:
            return

        new_grid = self.grid.copy()

        for y in range(self.rows):
            for x in range(self.cols):
                # Contar vecinos vivos
                neighbors = self.get_live_neighbors(x, y)

                if self.grid[y, x] == 1:  # Viva
                    if neighbors < 2 or neighbors > 3:
                        new_grid[y, x] = 0  # Muere por soledad o sobrepoblación
                elif self.grid[y, x] == 0:  # Muerta
                    if neighbors == 3:
                        new_grid[y, x] = 1  # Nace por reproducción

                # Reglas de contagio
                if self.grid[y, x] == 1 and self.rules.get("contagion_enabled", False):
                    if np.random.rand() < self.rules["contagion_prob_near"] and self.has_infected_neighbors(x, y):
                        new_grid[y, x] = 2  # Se infecta

                if self.grid[y, x] == 2:  # Infectada
                    if np.random.rand() < self.rules["recovery_prob"]:
                        new_grid[y, x] = 3  # Se recupera
                    elif np.random.rand() < self.rules["mortality_prob"]:
                        new_grid[y, x] = 0  # Muere

        self.grid = new_grid

    def get_live_neighbors(self, x, y):
        """Cuenta los vecinos vivos de una celda."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[ny, nx] in [1, 2]:
                count += 1
        return count

    def has_infected_neighbors(self, x, y):
        """Comprueba si una celda tiene vecinos infectados."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[ny, nx] == 2:
                return True
        return False

    def draw_grid(self):
        """Dibuja el tablero en la pantalla."""
        for y in range(self.rows):
            for x in range(self.cols):
                color = COLOR_DEAD_CELL
                if self.grid[y, x] == 1:
                    color = COLOR_LIVE_CELL
                elif self.grid[y, x] == 2:
                    color = COLOR_INFECTED_CELL
                elif self.grid[y, x] == 3:
                    color = (0, 255, 0)  # Verde para recuperadas
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                )

    def run(self):
        """Bucle principal del juego."""
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            self.update_grid()
            self.screen.fill(COLOR_BACKGROUND)
            self.draw_grid()
            pygame.display.flip()
            clock.tick(FPS)

