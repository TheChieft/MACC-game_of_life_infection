import pygame
import numpy as np
import time
import random
import modulo_1


# Inicializa Pygame
pygame.init()

# Tamaño de los valores
WIDTH, HEIGHT = 800, 800
nX, nY, nV = 25, 25, 25
xSize = WIDTH/nX
ySize = HEIGHT/nY

# Colores de las celulas 
LIVE_COLOR = (255,255,255)
DEAD_COLOR = (128,128,128)
INFECTED_COLOR = (255,0,0)

# Crear la ventana 
screen = pygame.display.set_mode([WIDTH,HEIGHT])
BG_COLOR = (10,10,10) # Define background color

# Crea las celulas / Celdas vivas = 1; Celdas muertas = 0
status = np.zeros((nX,nY)) # Inicializa las celulas (todas las celulas empiezan muertas)

#Crea el virus en una posicion aleatoria
virus_x = random.randint(0, WIDTH)
virus_x_s = WIDTH/nV
virus_y = random.randint(0, HEIGHT)
virus_y_s = HEIGHT/nV

# Crea el contador en la parte superior del codigo
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
texty = 10

# define nuevos atributos para la superficie. 
def show_poblacion(x,y):
    score = font.render("cells: "+str(poblacion),True,(255,255,255))
    screen.blit(score,(x,y))
	

# Funcion que almacena datos importantes en un archivo
def datos_imp(poblacion,infectados,segundos):
    file = open("datos.txt", "w")
    file.write("num celulas vivas: " + str(poblacion)+"\n")
    file.write("num celulas infectadas: " + str(infectados)+"\n")
    file.write("tiempo transcurrido: " + str(segundos)+"\n")
    file.close()


pauseRun = False
running = True



while running:
    poblacion = 0
    infectados = 1
    newStatus = np.copy(status) # Copia status para poder tomar nuevos valores en la simulacion.

    #Dibuja el virus en la cuadricula 
    poly_virus = [(virus_x*virus_x_s,virus_y*virus_y_s), #vector de 2D dimensiones para el virus.
                    ((virus_x+1)*virus_x_s,virus_y*virus_y_s),
                    ((virus_x+1)*virus_x_s,(virus_y+1)*virus_y_s),
                    (virus_x*virus_x_s,(virus_y+1)*virus_y_s)]

    pygame.draw.polygon(screen, INFECTED_COLOR, poly_virus)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            pauseRun = not pauseRun
            
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            x, y = int(np.floor(posX/xSize)), int(np.floor(posY/ySize))
            newStatus[x,y] = np.abs(newStatus[x,y]-1)
            newStatus[x,y] = not mouseClick[2]

    #Se crean unas listas vacias y un diccionario para almacenar valores relacionados, en este caso
    #numero de infectados y tiempo transcurrido.
    lista_sec = []
    lista = []
    segundos = time.time()
    y = lista_sec.append(segundos)
    lista.append(y)
   
    dic_po_s = {}

    screen.fill(BG_COLOR) # Limpia la ventana 

    for x in range(0,nX):
        for y in range(0,nY):


            if not pauseRun:

                

                # Numero de vecinos
                nNeigh = status[(x-1)%nX,(y-1)%nY] + status[(x)%nX,(y-1)%nY] + \
                        status[(x+1)%nX,(y-1)%nY] + status[(x-1)%nX,(y)%nY] + \
                        status[(x+1)%nX,(y)%nY] + status[(x-1)%nX,(y+1)%nY] + \
                         status[(x)%nX,(y+1)%nY] + status[(x+1)%nX,(y+1)%nY]


                # Definicion de reglas

                # Rule 1: Una celula muerta con 3 vecinas revive
                if status[x,y] == 0 and nNeigh==3:
                    newStatus[x,y] = 1

                # Rule 2: Una celula viva con mas de 3 vecinos o menos de 2 muere
                elif status[x,y] == 1 and (nNeigh < 2 or nNeigh > 3):
                    newStatus[x,y] = 0

                #Rule 3: Una celula viva que esta en la misma posicion que el virus, ret
                elif status[x,y] == 1 and nX == virus_x:
                    newStatus[x,y] = 2

            
            #Dibuja la celula en la cuadricula
            poly = [(x*xSize,y*ySize), #vector de 2D dimensiones para las celulas.
                    ((x+1)*xSize,y*ySize),
                    ((x+1)*xSize,(y+1)*ySize),
                    (x*xSize,(y+1)*ySize)]

            #Casos donde las celulas moriran, viviran o se infectaran. 

            if newStatus[x,y] == 1:
                poblacion += 1
                pygame.draw.polygon(screen,LIVE_COLOR,poly)
            elif newStatus[x,y] == 2:
                infectados += 1
                pygame.draw.polygon(screen,INFECTED_COLOR,poly_virus)
                dic_po_s[segundos] = infectados
            else:
                pygame.draw.polygon(screen,DEAD_COLOR,poly)



    status = np.copy(newStatus)
    time.sleep(0.1)
    show_poblacion(textX,texty)
    pygame.display.flip()


#Se llaman a las funciones cuyo objetivo es utilizar la informacion para generar graficas: 

datos_imp(poblacion, infectados, segundos)
blancas = poblacion - infectados
lista_total = modulo_1.lista(segundos, infectados, blancas, poblacion)
porcentajes = modulo_1.porcentajes(lista_total)
modulo_1.pie_graph(porcentajes)


pygame.quit()
print(infectados)
print(dic_po_s)
