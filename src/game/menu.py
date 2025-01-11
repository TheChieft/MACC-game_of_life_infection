import pygame
import numpy as np
import random
from src.utils.constants import *

class BaseMenu:
    def __init__(self, game):
        self.game = game
        self.options = []  # Lista de opciones (texto, acción)
        self.selected_index = 0
        self.font = pygame.font.Font(FONT_PATH, 20)
        self.title_font = pygame.font.Font(FONT_PATH, 40)


    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.game.screen.blit(text_surface, text_rect)

    def draw_cursor(self, x, y):
        pygame.draw.polygon(self.game.screen, COLOR_CURSOR, [
            (x, y - 10), (x + 10, y), (x, y + 10)
        ])

    def move_cursor(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.options)

    def select_option(self):
        _, action = self.options[self.selected_index]
        action()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.go_back()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_cursor(-1)
                elif event.key == pygame.K_DOWN:
                    self.move_cursor(1)
                elif event.key == pygame.K_RETURN:
                    self.select_option()

    def go_back(self):
        self.game.running = False

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

    def display_menu(self):
        self.running = True
        while self.running:
            self.game.screen.fill(COLOR_BACKGROUND)
            self.draw_background_simulation()

            # Ajustar el título y las opciones al nuevo diseño
            self.draw_text("GAME OF LIFE", self.title_font, (255, 255, 255), self.game.screen_w // 2, 50)

            for index, (text, _) in enumerate(self.options):
                color = (255, 255, 255) if index == self.selected_index else (180, 180, 180)
                self.draw_text(text, self.font, color, self.game.screen_w // 2, 150 + index * 40)

            self.draw_cursor(self.game.screen_w // 2 - 150, 150 + self.selected_index * 40)

            pygame.display.flip()
            self.handle_input()


    def start_game(self):
        self.game.running = True
        self.game.playing = True

    def open_settings(self):
        settings_menu = SettingsMenu(self.game)
        settings_menu.display_menu()

    def exit_game(self):
        self.game.running = False
        pygame.quit()
        quit()


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
class SettingsMenu(BaseMenu):
    def __init__(self, game):
        super().__init__(game)
        self.update_options()

    def update_options(self):
        contagion_status = "activado" if self.game.contagion_enabled else "desactivado"
        self.options = [
            ("Tamaño del Mapa", self.adjust_map_size_display),
            (f"Activar Enfermedad ({contagion_status})", self.toggle_contagion),
            ("Reglas de Contagio", self.modify_rules),
            ("Restablecer Predeterminadas", self.reset_defaults),
            ("Volver", self.go_back)
        ]

    def display_menu(self):
        self.running = True
        while self.running:
            # Actualizar las opciones del menú para reflejar el estado actual
            self.update_options()
            
            # Reutilizar el fondo de simulación del MainMenu
            self.game.screen.fill(COLOR_BACKGROUND)
            self.draw_background_simulation()

            # Dibujar el título del menú de configuración
            self.draw_text("Configuración", self.title_font, (255, 255, 255), self.game.screen_w // 2, 50)

            # Dibujar las opciones del menú
            for index, (text, _) in enumerate(self.options):
                color = (255, 255, 255) if index == self.selected_index else (180, 180, 180)
                self.draw_text(text, self.font, color, self.game.screen_w // 2, 150 + index * 40)

            # Alinear el cursor con el texto
            cursor_x_offset = -120  # Ajusta este valor según el diseño
            self.draw_cursor(self.game.screen_w // 2 + cursor_x_offset, 150 + self.selected_index * 40)

            pygame.display.flip()
            self.handle_input()

    def toggle_contagion(self):
        self.game.contagion_enabled = not self.game.contagion_enabled
        estado = "activado" if self.game.contagion_enabled else "desactivado"
        print(f"Contagio {estado}")

    def draw_background_simulation(self):
        """Reutiliza el fondo del MainMenu."""
        cell_size = 20
        cols = self.game.screen_w // cell_size
        rows = self.game.screen_h // cell_size
        grid = np.random.choice([0, 1], size=(rows, cols), p=[0.85, 0.15])

        for y in range(rows):
            for x in range(cols):
                color = (50, 50, 50) if grid[y, x] == 1 else (20, 20, 20)
                pygame.draw.rect(self.game.screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    def adjust_map_size_display(self):
        sizes = [("800x600", (800, 600)), ("1024x768", (1024, 768)), ("1280x720", (1280, 720))]
        selected_index = 0  # Índice para el tamaño seleccionado

        running = True
        while running:
            self.game.screen.fill(COLOR_BACKGROUND)
            self.draw_background_simulation()

            self.draw_text("Elige un tamaño", self.title_font, (255, 255, 255), self.game.screen_w // 2, 50)

            for index, (label, _) in enumerate(sizes):
                color = (255, 255, 255) if index == selected_index else (180, 180, 180)
                self.draw_text(label, self.font, color, self.game.screen_w // 2, 150 + index * 40)

            # Mostrar cursor alineado
            cursor_x_offset = -120
            self.draw_cursor(self.game.screen_w // 2 + cursor_x_offset, 150 + selected_index * 40)

            pygame.display.flip()

            # Manejo de entradas
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(sizes)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(sizes)
                    elif event.key == pygame.K_RETURN:
                        # Cambiar el tamaño del mapa al seleccionado
                        selected_size = sizes[selected_index]
                        self.game.screen_w, self.game.screen_h = selected_size[1]
                        pygame.display.set_mode(selected_size[1])
                        print(f"Tamaño cambiado a {selected_size[0]}")
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

    def modify_rules(self):
        print("Modificar reglas de contagio: Placeholder")

    def reset_defaults(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT, CONTAGION_ENABLED, CONTAGION_PROB_NEAR, CONTAGION_PROB_DISTANT
        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
        CONTAGION_ENABLED = True
        CONTAGION_PROB_NEAR = 0.3
        CONTAGION_PROB_DISTANT = 0.1
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Opciones restablecidas a los valores predeterminados.")

    def go_back(self):
        self.running = False
