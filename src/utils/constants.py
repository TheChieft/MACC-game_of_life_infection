# constants.py

# Activar o desactivar la enfermedad
CONTAGION_ENABLED = True

# Configuración general del juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 25
FPS = 60

# Colores
COLOR_BACKGROUND = (0, 0, 0)
COLOR_LIVE_CELL = (255, 255, 255)
COLOR_DEAD_CELL = (50, 50, 50)
COLOR_INFECTED_CELL = (255, 0, 0)
COLOR_CURSOR = (255, 255, 255)

# Rutas de recursos
FONT_PATH = "assets/fuentes/Fuente.ttf"

# Reglas de contagio
CONTAGION_PROB_NEAR = 0.3  # Probabilidad de contagio cercano
CONTAGION_PROB_DISTANT = 0.1  # Probabilidad de contagio a distancia
RECOVERY_PROB = 0.2  # Probabilidad de recuperación
MORTALITY_PROB = 0.05  # Probabilidad de que una celda infectada muera
IMMUNITY_DURATION = 10  # Tiempo de inmunidad tras recuperarse (en ciclos)

# Parámetros del mapa
GRID_ROWS = SCREEN_HEIGHT // CELL_SIZE
GRID_COLS = SCREEN_WIDTH // CELL_SIZE
