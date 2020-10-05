import pygame, sys
from pygame import quit

pygame.init()

##CONSTANTES

#creacion de costantes utilizadas para los individuos/cell
blanco=(255,255,255) #color blanco para celulas vivas
rojo=(255,0,0) #color rojo para celulas infectadas
# " " el color para celulas muertas sera el del fondo



'''
definir caracteristicas de la ventana
'''
def windows():      #Creacion de ventana
    WIDTH, HEIGHT = 800, 800  #Ancho y alto de la ventana
    screen = pygame.display.set_mode([WIDTH,HEIGHT]) #definir el tamaño de la ventana
    bg_color=(0,0,0) #Color del fondo de la ventana (negro)
    pygame.display.set_caption("Game of life: Pandemic simulator") #titulo de la ventana



'''
Mantener abierta la ventana
'''
def windowsrun(): 
    windows() #llamar a la funcion de crear ventana
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update() #actualizacion de ventana por nuevos sucesos
        
windowsrun()