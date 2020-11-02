# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 19:17:56 2020

@author: santi
"""
texto =("""¡Bienvenido a Virus Simulator!

Virus simulator es una herramienta para hacer simulaciones interactivas y analizar de forma dinámica el impacto de un virus en una población. El usuario juega a ser dios.  Basado en el juego de la vida, un autómata celular diseñado por el matemático británico John Horton Conway en 1970.

A continuación, se abrirá una cuadrícula de color negro, para iniciar a colocar las celulas debe undir la tecla SPACE y posteriormente hacer click con el mouse en cada cuadro hasta que se torne color blanco, luego de seleccionar las celdas deseadas oprima nuevamente la tecla SPACE. 

El virus se encuentra en un lugar aleatorio del espacio y podría entrar en contacto en cualquier momento con las células vivas. 

Durante la simulación, la célula podrá tomar los siguientes estados:

Célula viva:
Una célula viva con 2 o 3 células vecinas vivas sigue viva. Una célula muerta con exactamente 3 células vecinas vivas nace (es decir, al turno siguiente estará viva).

Célula infectada:
Una célula viva a cierta distancia del virus o otra célula infectada, se convertirá en una célula infectada. 

Célula muerta:
Una célula sin vecinos muere de soledad, una célula con más de 3 vecinos muere de sobrepoblación.

Al finalizar, se mostrarán al usuario unos datos recolectados durante la simulación, al igual que unas gráficas animadas.""")
print(texto)