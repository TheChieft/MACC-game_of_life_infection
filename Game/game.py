#FINAL_CODE

import pygame
import random
import time
import numpy as np
from src.game.menu import *
import sys


class GAME():
    def __init__(self,width=800,height=800, cell_size=25, LIVE_COLOR=(255,255,255),DEAD_COLOR = (128,128,128),INFECTED_COLOR = (255,0,0),BG_COLOR=(10,10,10)):
        pygame.init() #INICIALIZAR MODULOS PYGAME
        ###TAMAÑO
        self.cell_size = cell_size #tamaño de la celda
        ###COLORES
        self.live = LIVE_COLOR #color de celula viva
        self.dead = DEAD_COLOR #color de celula muerta
        self.infected= INFECTED_COLOR #color de celula enferma
        self.bg=BG_COLOR #color de fondo
        self.negro=(0,0,0) #color negro

        #VENTANA
        self.screen_w = width #tamaño ancho de la pantalla
        self.screen_h = height #tamaño de alto de la pantalla
        #CUADRICULA
        self.xSize = self.screen_w/self.cell_size #cantidad filas
        self.ySize = self.screen_h/self.cell_size #cantidad de columnas

        #self.display=pygame.surface((self.screen_w,self.screen_h))
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h)) #crear ventana

        #CELULAS
        self.status = np.zeros((self.cell_size,self.cell_size)) #satados del la celula por posicion en pantalla 
        #ESTADOS 
        self.pauseRun = False #DETERMINAR SI EL JUEGO SE HA PAUSADO
        self.running = True #TENERMINAR SI EL juego esta corriendo
        #Contadores
        self.poblacion = 0 #contador de celulas vivas al momento (inicializado en 0)
        self.infectados = 0 #contador de infectados al momento (inicializado en 0)

        #fuentes
        self.font = pygame.font.Font("freesansbold.ttf",32) #fuentes de contadores 
        self.font_titulo = pygame.font.get_default_font() #fuente del menu

        ##MENU *IMPORTANTE*
        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False #teclas de seleccion menu
        self.menu=Menu_screen(self) #HERENCIA DE Menu() DONDE ESTA LA VISTA DEL MENU
        self.menu_inicial=self.menu #COPIA DE LA HERENCIA
        self.display = pygame.Surface((self.screen_w,self.screen_h)) #CREAR UNA ZONA PARA MOSTRAR IMAGENES / TEXTOS

    #MENU
    def draw_text(self, text, size, x, y ): #DIBUJAR LETRAS EN PANTALLA
        font = pygame.font.Font(self.font_titulo,size) #FUENTE DE LETRAS
        text_surface = font.render(text, True, self.live) #PINTAR EN OTRA SURFACE
        text_rect = text_surface.get_rect() #RECTANGULO DEL MISMO TAMAÑO QUE LA PANTALLA
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    #JUEGO
    def pro_infected(self): #ESTA FUNCION GENERA UN PORCENTAJE DE CONTAGIO ENTRE LA CELULA MADRE Y SUS HIJAS
        x=random.random() #se genera un valor entre 0 y 1 para retornar la probabilidad de trasmicion de la enfermedad
        if x<=0.2: 
            return 2
        else:
            return 1    

    def Texto_en_juego(self,x,y,texto='',valor=True): #MOSTRAR DATOS EN PANTALLA
        if valor: #DATOS DE CANTIDAD DE CELULAS VIVAS AL MOMENTO
            score = self.font.render("cells: "+str(texto),True,(255,255,255))
            self.screen.blit(score,(x,y))
        elif valor == False: #DATOS DE CANTIDAD DE CELULAS CONTAGIADAS AL MOMENTO
            score = self.font.render("infected: "+str(texto),True,(255,255,255))
            self.screen.blit(score,(x,y))
        elif valor == None:
            font=pygame.font.Font(self.font_titulo,20)
            score = font.render("Pulse la tecla 'espacio' para pausar/correr el juego ",True,(255,255,255))
            self.screen.blit(score,(x,y))
    
    def cuadricula(self): #valores de cada cuadricula
        self.poly = [(self.x*self.xSize,self.y*self.ySize),
                            ((self.x+1)*self.xSize,self.y*self.ySize),
                            ((self.x+1)*self.xSize,(self.y+1)*self.ySize),
                            (self.x*self.xSize,(self.y+1)*self.ySize)] #valores para dibujar un cuadrados en la pantalla
    
    def Calcular_Numero_de_vecinos(self): #observar vecinos cernanos a una celula
        self.nNeigh = self.status[(self.x-1)%self.cell_size,(self.y-1)%self.cell_size] + self.status[(self.x)%self.cell_size,(self.y-1)%self.cell_size] + \
                                self.status[(self.x+1)%self.cell_size,(self.y-1)%self.cell_size] + self.status[(self.x-1)%self.cell_size,(self.y)%self.cell_size] + \
                                self.status[(self.x+1)%self.cell_size,(self.y)%self.cell_size] + self.status[(self.x-1)%self.cell_size,(self.y+1)%self.cell_size] + \
                                self.status[(self.x)%self.cell_size,(self.y+1)%self.cell_size] + self.status[(self.x+1)%self.cell_size,(self.y+1)%self.cell_size]
    
    def reglas_juego(self):
        ##REGLAS DEL JUEGO DE LA VIDA
        # Rule 1: Una celula muerta con 3 vecinas revive
        if (self.status[self.x,self.y] == 0 or self.status[self.x,self.y]==2) and self.nNeigh==3:
            self.newStatus[self.x,self.y] = self.pro_infected()

        # Rule 2: Una celula viva/enferma con mas de 3 vecinos o menos de 2 muere
        elif (self.status[self.x,self.y] == 1 or self.status[self.x,self.y]==2) and (self.nNeigh < 2 or self.nNeigh > 3):
            self.newStatus[self.x,self.y] = 0

        ##REGLAS PUESTAS
    
    def definir_estados(self): #actualizar los estados de una celda con el color de la celula
        if self.newStatus[self.x,self.y] == 1: #si el estado de la celda es 1 se pinta con el color de celula viva (self.live)
            self.poblacion += 1
            pygame.draw.polygon(self.screen,self.live,self.poly,0)

        elif self.newStatus[self.x,self.y] == 2: #si el estado de la celda es 2 se pinta con el color de celula enferma (self.live)
            self.infectados += 1
            pygame.draw.polygon(self.screen,self.infected,self.poly,0)
        else: #si el estado de la celula es otro (0) se pintara de color de celula muerta (self.dead)
            pygame.draw.polygon(self.screen,self.dead,self.poly,1)

    def events(self): #obtener los eventos del mause en pantalla y de teclas
        for event in pygame.event.get():
                if event.type == pygame.QUIT: #si se selecciona la x en el la venta de windows se cierra el programa
                    self.run_menu= False
                    self.running = False
                    self.menu_inicial.run_display = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: #si se presiona alguna tecla se pausa el juego
                    if event.key == pygame.K_RETURN:
                        self.START_KEY = True
                    if event.key == pygame.K_DOWN:
                        self.DOWN_KEY = True
                    if event.key == pygame.K_UP:
                        self.UP_KEY = True
                    if event.key == pygame.K_SPACE: #la tecla de espacio genera una pausa al juego
                        self.pauseRun = not self.pauseRun

                self.mouseClick = pygame.mouse.get_pressed() #guarda los click del mouse

                if sum(self.mouseClick) > 0: #si se presiona el mouse se cambia el valor de una celda a una celula viva
                    self.posX, self.posY = pygame.mouse.get_pos()
                    self.x, self.y = int(np.floor(self.posX/self.xSize)), int(np.floor(self.posY/self.ySize))
                    self.newStatus[self.x,self.y] = np.abs(self.newStatus[self.x,self.y]-1)
                    self.newStatus[self.x,self.y] = not self.mouseClick[2]

    def crear_y_actualizar_cuadricula(self):
        for self.x in range(0,self.cell_size): #Para filas
            for self.y in range(0,self.cell_size): #para columnas

                if not self.pauseRun: # si no esta pausado 
                    self.Calcular_Numero_de_vecinos() #Observar a los vecinos de cada celda
                    self.reglas_juego() #reglas definidas
                        
                self.cuadricula() #crear cuadrados unitarios
                self.definir_estados() #Actualizar los estados de las celdas y celulas
    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def run(self): #CORRE EL JUEGO
        while self.running: #LOOP DE VENTANA
            self.newStatus = np.copy(self.status) #COPIAR EL ULTIMO ESTADO DE LA CELDA

            #CONTADORES
            self.poblacion = 0  #contador de celulas vivas
            self.infectados = 0 #contador de celulas infectadas

            self.events() #reconocer los eventos sucedidos en pantalla y teclado
            self.screen.fill(self.bg) #al actualizar la pantalla se usa el color de fondo para esconder los nuevos valores

            self.crear_y_actualizar_cuadricula() #crear la cuadricula y obtener eventos y actualizar celdas

            self.status = np.copy(self.newStatus) #Obetener el ultimo estado de las celdas
            time.sleep(0.1)

            #Mostrar contadores
            self.Texto_en_juego(10,10,self.poblacion)
            self.Texto_en_juego(150,10,self.infectados,False)
            self.Texto_en_juego(10,775,'',None)

            pygame.display.flip() #actualizar pantalla
            self.reset_keys()


