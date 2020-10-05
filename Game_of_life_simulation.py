import pygame, sys

pygame.init()

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

windowsrun()