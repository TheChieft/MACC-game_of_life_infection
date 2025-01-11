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

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game of Life Infection")

        # Crear el tablero
        self.cols = self.screen_width // self.cell_size
        self.rows = self.screen_height // self.cell_size
        self.grid = np.zeros((self.rows, self.cols), dtype=int)

        # Manejo de inmunidad
        self.immunity_counters = np.zeros((self.rows, self.cols), dtype=int)

        self.populate_grid()

        # Variables para estadísticas (si quieres rastrear total infectados, etc.)
        self.total_infected_ever = 0

    def populate_grid(self):
        """Inicializa el tablero con celdas vivas y muertas aleatoriamente."""
        self.grid = np.random.choice([0, 1], size=(self.rows, self.cols), p=[0.85, 0.15])
        self.immunity_counters.fill(0)

    def handle_events(self):
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
                        if self.rules.get("contagion_enabled", False):
                            self.grid[row, col] = 2  # Infectar manualmente
                            self.total_infected_ever += 1
                elif event.button == 3:  # Clic derecho
                    self.grid[row, col] = 0  # Eliminar célula
                    self.immunity_counters[row, col] = 0


    def update_grid(self):
        if self.paused:
            return

        new_grid = self.grid.copy()
        new_immunity = self.immunity_counters.copy()

        for y in range(self.rows):
            for x in range(self.cols):
                current_state = self.grid[y, x]
                neighbors = self.get_live_neighbors(x, y)

                # 1) Aplicar reglas clásicas de Conway (para estados 1 y 3, si deseas) 
                if current_state in [1, 3]:  
                    # Muere por soledad o sobrepoblación
                    if neighbors < 2 or neighbors > 3:
                        new_grid[y, x] = 0
                        new_immunity[y, x] = 0
                elif current_state == 0:
                    # Nace una célula (estado 1) si tiene 3 vecinos vivos/infectados/recuperados
                    if neighbors == 3:
                        new_grid[y, x] = 1
                        new_immunity[y, x] = 0

                # 2) Reglas de infección
                if current_state == 1 and self.rules.get("contagion_enabled", False):
                    # Probabilidad de contagio si hay infectados cerca
                    if np.random.rand() < self.rules["contagion_prob_near"] and self.has_infected_neighbors(x, y):
                        new_grid[y, x] = 2
                        self.total_infected_ever += 1

                # 3) Estado infectado (2)
                if current_state == 2:
                    # Se recupera con cierta probabilidad
                    if np.random.rand() < self.rules["recovery_prob"]:
                        new_grid[y, x] = 3
                        new_immunity[y, x] = 0  # Comienza el conteo de inmunidad
                    # Muere con probabilidad
                    elif np.random.rand() < self.rules["mortality_prob"]:
                        new_grid[y, x] = 0
                        new_immunity[y, x] = 0

                # 4) Estado recuperado (3) → contar inmunidad
                if current_state == 3:
                    # Ya aplicamos las reglas de Conway al inicio (si deseas)
                    # Incrementamos el contador de inmunidad
                    new_immunity[y, x] += 1
                    # Chequeamos si superó IMMUNITY_DURATION
                    if new_immunity[y, x] >= IMMUNITY_DURATION:
                        # Vuelve a ser 1 (viva), susceptible de infectarse
                        new_grid[y, x] = 1
                        new_immunity[y, x] = 0

        self.grid = new_grid
        self.immunity_counters = new_immunity

    def get_live_neighbors(self, x, y):
            """Cuenta los vecinos que están en estado 1, 2 o 3 (vivo, infectado o recuperado)."""
            directions = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1),           (0, 1),
                          (1, -1),  (1, 0),  (1, 1)]
            count = 0
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    # Consideramos 'vivo'(1), 'infectado'(2) y 'recuperado'(3) como vecinos "vivos" para Conway
                    if self.grid[ny, nx] in [1, 2, 3]:
                        count += 1
            return count

    def has_infected_neighbors(self, x, y):
        """Comprueba si hay vecinos infectados (2)."""
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                if self.grid[ny, nx] == 2:
                    return True
        return False

    def draw_grid(self):
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
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 200),
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    1,
                )

    def draw_instructions(self):
        font = pygame.font.Font(None, 24)
        instructions = [
            "P: Pausar/Reanudar",
            "R: Reiniciar",
            "ESC: Volver al menú",
            "Click izq: Crear / Infectar célula",
            "Click der: Eliminar célula",
        ]
        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, self.screen_height - (len(instructions) - i) * 20))

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
        clock = pygame.time.Clock()
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
            alive = np.sum(self.grid == 1) + np.sum(self.grid == 3)  # sumamos 1 y 3 como "vivas"
            infected = np.sum(self.grid == 2)
            recovered = np.sum(self.grid == 3)
            dead = self.rows * self.cols - (alive + infected)

            data["iteration"].append(iteration)
            data["alive"].append(alive)
            data["infected"].append(infected)
            data["recovered"].append(recovered)
            data["dead"].append(dead)

            self.screen.fill(COLOR_BACKGROUND)
            self.draw_grid()
            self.draw_instructions()
            self.draw_realtime_chart(data, 10, 10, 150, 100)
            pygame.display.flip()

            clock.tick(FPS // 2)
            iteration += 1

        # GUARDAR DATOS (ver parte 2)
        df = pd.DataFrame(data)
        output_file = "analysis/game_data.csv"  # Ruta sugerida (crea la carpeta si no existe)
        df.to_csv(output_file, index=False)
        print(f"Datos del juego guardados en: {output_file}")

        # Resumen final (ejemplo)
        max_infected = df["infected"].max()
        it_max_infected = df["infected"].idxmax()
        final_alive = df["alive"].iloc[-1]
        final_infected = df["infected"].iloc[-1]
        final_recovered = df["recovered"].iloc[-1]
        final_dead = df["dead"].iloc[-1]

        print("\n--- Resumen Estadístico ---")
        print(f"Partida con {iteration} iteraciones totales")
        print(f"Máximo de infectados: {max_infected} (iteración {it_max_infected})")
        print(f"Vivas finales: {final_alive} | Infectadas finales: {final_infected}")
        print(f"Recuperadas finales: {final_recovered} | Muertas finales: {final_dead}")
        print("--------------------------------\n")

        pygame.quit()
        # Fin del Game.run()
