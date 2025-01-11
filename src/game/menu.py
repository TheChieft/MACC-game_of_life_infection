import pygame
import numpy as np
import random

class BaseMenu:
    def __init__(self, game):
        self.game = game
        self.options = []  # Lista de opciones (texto, acción)
        self.selected_index = 0
        self.font = pygame.font.Font("assets/fuentes/Fuente.ttf", 30)
        self.title_font = pygame.font.Font("assets/fuentes/Fuente.ttf", 60)

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.game.screen.blit(text_surface, text_rect)

    def draw_cursor(self, x, y):
        pygame.draw.polygon(self.game.screen, (255, 255, 255), [
            (x, y - 10), (x + 10, y), (x, y + 10)
        ])

    def move_cursor(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.options)

    def select_option(self):
        _, action = self.options[self.selected_index]
        action()

    def display_menu(self):
        raise NotImplementedError("display_menu must be implemented by subclasses")

class MainMenu(BaseMenu):
    def __init__(self, game):
        super().__init__(game)
        self.options = [
            ("Jugar", self.start_game),
            ("Configuración", self.open_settings),
            ("Salir", self.exit_game)
        ]

    def start_game(self):
        self.game.running = True
        self.game.playing = True

    def open_settings(self):
        print("Abrir configuración (placeholder)")

    def exit_game(self):
        self.game.running = False
        pygame.quit()
        quit()

    def display_menu(self):
        self.running = True
        while self.running:
            self.game.screen.fill((0, 0, 0))  # Fondo negro temporal
            self.draw_background_simulation()  # Fondo dinámico

            self.draw_text("GAME OF LIFE", self.title_font, (255, 255, 255), self.game.screen_w // 2, 100)

            for index, (text, _) in enumerate(self.options):
                color = (255, 255, 255) if index == self.selected_index else (180, 180, 180)
                self.draw_text(text, self.font, color, self.game.screen_w // 2, 200 + index * 50)

            self.draw_cursor(self.game.screen_w // 2 - 100, 200 + self.selected_index * 50)

            pygame.display.flip()
            self.handle_input()

    def draw_background_simulation(self):
        cell_size = 20
        cols = self.game.screen_w // cell_size
        rows = self.game.screen_h // cell_size
        grid = np.random.choice([0, 1], size=(rows, cols), p=[0.85, 0.15])

        for y in range(rows):
            for x in range(cols):
                color = (50, 50, 50) if grid[y, x] == 1 else (20, 20, 20)
                pygame.draw.rect(self.game.screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_cursor(-1)
                elif event.key == pygame.K_DOWN:
                    self.move_cursor(1)
                elif event.key == pygame.K_RETURN:
                    self.select_option()
