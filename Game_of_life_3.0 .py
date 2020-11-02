#IMPORTS
import pygame 
import sys
from pygame.locals import *
import numpy as np
import time
import random
import modulo_1
import os 

#CLASS

#FUNCIONES
def draw_text(text, font, color, surface, x, y): #Pintar textos en pantalla
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center= (x, y)
    surface.blit(textobj, textrect)

# define nuevos atributos para la superficie. 
def show_poblacion(x,y,poblacion):
    score = font.render("cells: "+str(poblacion),True,(255,255,255))
    windows.blit(score,(x,y))

# Funcion que almacena datos importantes en un archivo
def datos_imp(poblacion,infectados,segundos):
    file = open("datos.txt", "w")
    file.write("num celulas vivas: " + str(poblacion)+"\n")
    file.write("num celulas infectadas: " + str(infectados)+"\n")
    file.write("tiempo transcurrido: " + str(segundos)+"\n")
    file.close()

def Rules():
    #variables para el BG
    velocidad=0.5
    posx=-400
    posy=0
    left=True

    while True:
        windows.fill(NEGRO) #rellenar el fondo de un color
        windows.blit(BG_menu,(posx,posy)) #poner el fondo del juego
        draw_text('Rules', font, NEGRO, windows, 400, 200)
        draw_text("Esto es una DEMO ",font,NEGRO,windows,400,300)
    
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
        
        pygame.display.update()
        mainClock.tick(60)


def Play():
   os.system("python game.py")
    #Dentro de os.system escriba la direccion del archivo game_of_life_virus.py 

def Menu():
    #variables para el BG
    velocidad=0.5
    posx=-400
    posy=0
    left=True
    #titulo
    Mi_titulo=Title_font_1.render("Game of Life",0,NEGRO)

    click = False

    while True: #crear y actualizar ventana

        windows.fill(NEGRO) #rellenar el fondo de un color
        windows.blit(BG_menu,(posx,posy)) #poner el fondo del juego

        """Titulo"""
        position_title=(200,100)

        windows.blit(Mi_titulo,position_title)

        """Mouse"""
        nx, ny = pygame.mouse.get_pos() #posicion del mouse

        """Botones"""
        button_Play = pygame.Rect(Mid, distance ,Cube_w,Cube_h)
        button_Rules = pygame.Rect(Mid, distance+100 ,Cube_w,Cube_h)
        button_exit=pygame.Rect(Mid, distance+200 , Cube_w,Cube_h)

        if button_Play.collidepoint((nx, ny)):
            if click:
                Play()
        if button_Rules.collidepoint((nx, ny)):
            if click:
                Rules()
        if button_exit.collidepoint((nx, ny)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(windows, GRIS, button_Play)
        pygame.draw.rect(windows, GRIS, button_Rules)
        pygame.draw.rect(windows, GRIS, button_exit)

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        #Mover el fondo de la imagen derecha a izquierda
        if left==True:
            if posx<1:
                posx+=velocidad
            else:
                left=False
        else:
            if posx>-600:
                posx-=velocidad
            else:
                left=True
    
        pygame.display.update()
        mainClock.tick(60)


#BOE-----------------------------x

pygame.init()

##CONSTANTES 

"""funetes de letra"""
Title_font_1=pygame.font.SysFont("Elephant",80)
Play_font = pygame.font.Font("freesansbold.ttf",32)
font = pygame.font.Font("freesansbold.ttf",32)

"""Otras constantes"""
mainClock = pygame.time.Clock()

#posicion mouse
nx, ny = pygame.mouse.get_pos() #posicion del mouse
"""COLORES"""

BLANCO=(255,255,255) #Celulas vivas
NEGRO=(0,0,0) #Celulas muertas
ROJO=(255,0,0) #Celulas enfermas
BG_COLOR = (10,10,10) # Define background color
GRIS=(10,10,10) #Celulas muertas

"""Caracteristicas ventana"""
WIDTH, HEIGHT = 800, 700
Windows_WH=(WIDTH, HEIGHT)

nX, nY = 80, 80
xSize = WIDTH/nX
ySize = HEIGHT/nY

Cube_w=200
Cube_h=50

Mid=int((WIDTH/2)-(200/2))
distance=int(300)

"""textos"""
Rules_text=" "
"""Fondo de menu"""
BG_menu=pygame.image.load("BG_.png")

#-#
windows = pygame.display.set_mode(Windows_WH) #Crear ventana del menu
pygame.display.set_caption("Game of Life")
click = False

Menu()
pygame.quit()