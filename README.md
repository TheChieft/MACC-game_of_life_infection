# MACC - Game of Life Infection
¡Bienvenido/a a MACC - Game of Life Infection! Este proyecto combina el clásico “Juego de la Vida” de Conway con una simulación de contagio inspirada en la pandemia de COVID-19. La idea es mostrar cómo se comporta una infección dentro de las reglas del famoso autómata celular, y recoger estadísticas de lo que sucede en tiempo real.

**Nota: El nombre MACC hace referencia a una iteración previa del proyecto. ¡Pero mantuvimos el nombre por nostalgia!**

## ⭐ Características
- **Reglas originales** del Juego de la Vida:
  - Una célula viva muere por soledad si tiene menos de 2 vecinos vivos.
  - Muere por sobrepoblación si tiene más de 3 vecinos vivos.
  - Una célula muerta nace si tiene exactamente 3 vecinos vivos.
- **Reglas de contagio** (opcionalmente activables/desactivables):
  - Una célula viva puede infectarse con cierta probabilidad si tiene vecinos infectados.
  - Una célula infectada puede:
    - Recuperarse con cierta probabilidad.
    - Morir por la infección (probabilidad de mortalidad).
  - Una célula recuperada tiene **inmunidad temporal** y, pasado ese tiempo, **vuelve a ser una célula viva normal**(susceptible de reinfectarse).
- **Interfaz interactiva** con menús de configuración:
  - Ajustar la tasa de contagio cercano/lejanía, la probabilidad de recuperación y mortalidad, etc.
  - Cambiar el tamaño de la ventana.
  - Activar/desactivar la enfermedad en cualquier momento.
- **Estadísticas en tiempo real**:
  - Se dibuja un minigráfico con la evolución de células vivas, infectadas, recuperadas y muertas.
- **Resumen estadístico** al terminar cada partida (se guarda en data/game_data.csv):
  - Número de iteraciones, pico de infectados, cantidad final de vivas, infectadas, recuperadas y muertas.

## ✨ Inspiración
Este proyecto nació durante la pandemia y tiene como motivación:

1. **Aprender** sobre autómatas celulares, en especial el clásico “Juego de la Vida” de John Conway.
2. **Experimentar** con un modelo sencillo de contagio, aproximándose ligeramente a lo que ocurrió en la pandemia de COVID-19.
3. **Recopilar datos** (nacimientos, infecciones, recuperaciones) y compararlos con la realidad.


_John Horton Conway (1937-2020) murió tristemente durante la pandemia de COVID-19. Este trabajo está dedicado a él, en memoria de su gran legado en la matemática recreativa y en la teoría de autómatas celulares._

## 📂 Estructura de Archivos
```bash

project_root/
├── assets/
│   └── fuentes/
│       └── Fuente.ttf          # Fuente de texto usada por Pygame
├── data/
│   └── game_data.csv           # Aquí se guardan las estadísticas de cada partida
├── src/
│   ├── utils/
│   │   └── constants.py        # Variables globales: colores, tamaño de celda, FPS, etc.
│   ├── game/
│   │   ├── main.py             # Archivo principal (inicia el menú y la ejecución del proyecto)
│   │   ├── menu.py             # Menús: MainMenu, SettingsMenu, etc.
│   │   ├── game.py             # Lógica del Juego de la Vida + infección
│   │   └── __init__.py
│   └── analysis/               # (Carpeta opcional para scripts o análisis más avanzados)
└── README.md                   # Este archivo
```

1. ```assets/fuentes```: contiene la tipografía utilizada.
2. ```data/```: donde se guarda game_data.csv con estadísticas de la última partida.
3. ```src/utils/constants.py```: configura constantes (colores, probabilidades por defecto, etc.).
4. ```src/game/main.py```: actúa como launcher del programa, arranca el menú principal.
5. ```src/game/menu.py```: contiene las diferentes pantallas de menú y la navegación entre ellas.
6. ```src/game/game.py```: la clase Game con toda la lógica del autómata, las reglas de infección y el bucle principal de renderizado.

## 🚀 Cómo Ejecutar
1. **Instalar dependencias** (Python 3, Pygame, Numpy, Pandas):
```
pip install pygame numpy pandas
```
2. **Posicionarte en la raíz del proyecto** y ejecutar:
```bash
# En Linux o Mac:
PYTHONPATH=. python src/game/main.py
# En Windows (opción 1):
set PYTHONPATH=.
python src\game\main.py
# En Windows (opción 2 - Powershell):
$env:PYTHONPATH="."
python src\game\main.py
```
3. **Interacción en el menú**:
- **Jugar**: te mete al Juego de la Vida con infección (si está activada).
- **Configuración**: cambiar el tamaño, activar contagio, modificar probabilidades, etc.
- **Salir**: finaliza la aplicación. 
### 💡 Controles del Juego

- **P:** Pausar/Reanudar la simulación.
- **R:** Reiniciar el tablero con una nueva disposición aleatoria.
- **ESC:** Volver al menú principal.
- **Click izquierdo **sobre una celda muerta: crear célula viva.
Si la celda era viva y la enfermedad está activada, se infecta.
- **Click derecho:** eliminar la célula que haya en esa posición.

Mientras el juego corre, puedes ver:

- **Gráfico en tiempo real** (opcional) en la parte superior izquierda con la evolución de vivos, infectados, recuperados y muertos.

## 📊 Estadísticas y Análisis

- Al cerrar una partida, se genera o sobrescribe el archivo data/game_data.csv.
- Contiene las columnas:
  - ```iteration```: número de iteración (tiempo discreto).
  - ```alive```: células vivas (incluidas las recuperadas).
  - ```infected```: cuántas están en estado de infección.
  - ```recovered```: cuántas se encuentran en estado recuperado (inmunes temporalmente).
  - ```dead```: total de celdas muertas.
Además, se imprime un **resumen** en la consola, con:

- ```Máximo de infectados``` y en qué iteración ocurrió.
- ```Vivas finales```, ```Infectadas finales```, ```Recuperadas finales``` y ```Muertas finales```.
  
---

## 🧪 Posibles Extensiones

- Ajustar dinámicamente la probabilidad de recuperación, mortalidad, contagio.
- Agregar distintos “tipos de virus” con diferentes parámetros.
- Mostrar gráficos más detallados (matplotlib, scripts en la carpeta analysis).
- Implementar un modelo más cercano a la epidemiología (SIR, SEIR...).

## 🙌 Agradecimientos
- **John Horton Conway** por su legendaria contribución a la matemática y la creación de este maravilloso juego. Falleció en abril de 2020, dejando un enorme legado. ¡Gracias por tu genialidad!
- **Ana Karina**, colaboradora clave en etapas tempranas del proyecto. ¡Tu apoyo fue fundamental!
- A toda la comunidad de Python, Pygame, NumPy y pandas.

**¡Gracias por visitar este proyecto!**

Siéntete libre de abrir Issues, hacer forks y contribuir con mejoras. El mundo de la simulación y los autómatas celulares es infinito.