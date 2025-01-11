import pygame
import numpy as np
import pandas as pd
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
              elif event.key == pygame.K_ESCAPE:  # Volver al menú principal
                  self.running = False
          elif event.type == pygame.MOUSEBUTTONDOWN:
              x, y = event.pos
              col = x // self.cell_size
              row = y // self.cell_size

              if event.button == 1:  # Clic izquierdo
                  if self.grid[row, col] == 0:
                      self.grid[row, col] = 1  # Crear célula viva
                  elif self.grid[row, col] == 1:
                      if self.rules.get("contagion_enabled", False):  # Infectar si está habilitado
                          self.grid[row, col] = 2
              elif event.button == 3:  # Clic derecho
                  self.grid[row, col] = 0  # Eliminar célula


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
        """Dibuja el tablero en la pantalla con líneas de separación."""
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
                # Dibujar líneas de separación
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 200),  # Color de las líneas
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    1,
                )

    def draw_instructions(self):
      """Dibuja las instrucciones en la parte inferior de la pantalla."""
      font = pygame.font.Font(None, 24)
      instructions = [
          "P: Pausar/Reanudar",
          "R: Reiniciar",
          "ESC: Volver al menú",
          "Clic izquierdo: Crear/Infectar célula",
          "Clic derecho: Eliminar célula",
      ]
      for i, text in enumerate(instructions):
          text_surface = font.render(text, True, (255, 255, 255))
          self.screen.blit(text_surface, (10, self.screen_height - (len(instructions) - i) * 20))

      # Mostrar si la enfermedad está habilitada
      contagion_status = "ON" if self.rules.get("contagion_enabled", False) else "OFF"
      status_surface = font.render(f"Contagio: {contagion_status}", True, (255, 255, 0))
      self.screen.blit(status_surface, (10, self.screen_height - (len(instructions) + 1) * 20))

    def draw_realtime_chart(self, data_dict, pos_x, pos_y, width, height, max_points=100):
      """
      Dibuja un gráfico lineal en tiempo real de las últimas 'max_points' iteraciones.
      :param data_dict: diccionario con listas: { "alive": [...], "infected": [...], etc. }
      :param pos_x, pos_y: coordenadas donde se dibujará el gráfico
      :param width, height: dimensiones del rectángulo del gráfico
      :param max_points: cuántos puntos recientes mostrar
      """
      # 1) Obtener los datos más recientes
      # asumiendo todas las listas tienen la misma longitud
      total_cells = self.rows * self.cols
      length = len(data_dict["alive"])
      start = max(0, length - max_points)  # para no pasarnos
      # Cortamos los datos para graficar sólo la ventana
      alive_data = data_dict["alive"][start:]
      infected_data = data_dict["infected"][start:]
      recovered_data = data_dict["recovered"][start:]
      dead_data = data_dict["dead"][start:]

      # 2) Definir escalas
      # Eje X: de 0 a max_points (o menos si no hay tantas iteraciones)
      # Eje Y: de 0 a total_cells
      # Convertimos coordenadas de (iteración, valor) a (px, px)
      def to_screen_coords(i, val):
        # i va de 0..len(alive_data)-1
        # val va de 0..total_cells
        # x en pantalla:
        x_screen = pos_x + (i / (max_points - 1)) * width if (max_points > 1) else pos_x
        # y en pantalla (invertido, 0 arriba):
        y_screen = pos_y + height - (val / total_cells) * height
        return (x_screen, y_screen)

      # 3) Dibujar ejes (opcional)
      pygame.draw.rect(self.screen, (50, 50, 50), (pos_x, pos_y, width, height), 1)

      # 4) Dibujar cada línea
      # Aquí usamos un color distinto para cada lista de datos
      # definimos una función para dibujar la línea iterando de i a i+1
      def draw_line(data_list, color):
        for i in range(len(data_list)-1):
          p1 = to_screen_coords(i, data_list[i])
          p2 = to_screen_coords(i+1, data_list[i+1])
          pygame.draw.line(self.screen, color, p1, p2, 2)

      draw_line(alive_data, (0, 255, 255))     # celeste para vivos
      draw_line(infected_data, (255, 0, 0))   # rojo para infectados
      draw_line(recovered_data, (0, 255, 0))  # verde para recuperados
      draw_line(dead_data, (128, 128, 128))   # gris para muertos

      # 5) Dibujar la leyenda
      font = pygame.font.Font(None, 16)
      legend_items = [
        ("Vivos", (0, 255, 255)),
        ("Infectados", (255, 0, 0)),
        ("Recuperados", (0, 255, 0)),
        ("Muertos", (128, 128, 128)),
      ]
      for i, (label, color) in enumerate(legend_items):
        text_surface = font.render(label, True, color)
        self.screen.blit(text_surface, (pos_x + width + 10, pos_y + i * 20))



    def run(self):
        """Bucle principal del juego."""
        clock = pygame.time.Clock()
# Variables para estadísticas
        data = {
            "iteration": [],
            "alive": [],
            "infected": [],
            "recovered": [],
            "dead": [],
        }
        iteration = 0

        while self.running:
            self.handle_events()
            self.update_grid()

            # Recoger estadísticas
            alive = np.sum(self.grid == 1)
            infected = np.sum(self.grid == 2)
            recovered = np.sum(self.grid == 3)
            dead = self.rows * self.cols - (alive + infected + recovered)

            data["iteration"].append(iteration)
            data["alive"].append(alive)
            data["infected"].append(infected)
            data["recovered"].append(recovered)
            data["dead"].append(dead)

            self.screen.fill(COLOR_BACKGROUND)
            self.draw_grid()
            self.draw_instructions()
            # Justo antes de pygame.display.flip()
            self.draw_realtime_chart(data,
                pos_x=self.screen_width - 220, 
                pos_y=10,
                width=120,
                height=80,
                max_points=100
            )

            pygame.display.flip()

            clock.tick(FPS // 4)
            iteration += 1

        # Guardar datos al final
        df = pd.DataFrame(data)
        df.to_csv("/data/game_data.csv", index=False)
        print("Datos del juego guardados en game_data.csv")

        # Hacer un pequeño resumen
        max_infected = df["infected"].max()
        iteration_of_max_infected = df["infected"].idxmax()
        final_alive = df["alive"].iloc[-1]
        final_infected = df["infected"].iloc[-1]
        final_recovered = df["recovered"].iloc[-1]
        final_dead = df["dead"].iloc[-1]

        print("\n--- Resumen Estadístico ---")
        print(f"Máximo de infectados: {max_infected} (en iteración {iteration_of_max_infected})")
        print(f"Vivas finales: {final_alive} | Infectadas finales: {final_infected}")
        print(f"Recuperadas finales: {final_recovered} | Muertas finales: {final_dead}")
        print("--------------------------------\n")
