#FINAL_CODE

import pygame
import sys
from pygame.locals import *
import pygame
import modulo_1 as md 
from PIL import Image
from game_datas import GAME
game=GAME()

class Opcion:

    def __init__(self, fuente, titulo, x, y, paridad, funcion_asignada):
        self.imagen_normal = fuente.render(titulo, 1, (0, 0, 0))
        self.imagen_destacada = fuente.render(titulo, 1, (200, 0, 0))
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.x = 500 * paridad
        self.rect.y = y
        self.funcion_asignada = funcion_asignada
        self.x = float(self.rect.x)

    def actualizar(self):
        destino_x = 105
        self.x += (destino_x - self.x) / 5.0
        self.rect.x = int(self.x)

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

    def destacar(self, estado):
        if estado:
            self.image = self.imagen_destacada
        else:
            self.image = self.imagen_normal

    def activar(self):
        self.funcion_asignada()


class Cursor:

    def __init__(self, x, y, dy):
        self.image = pygame.image.load('cursor.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.y_inicial = y
        self.dy = dy
        self.y = 0
        self.seleccionar(0)

    def actualizar(self):
        self.y += (self.to_y - self.y) / 10.0
        self.rect.y = int(self.y)

    def seleccionar(self, indice):
        self.to_y = self.y_inicial + indice * self.dy

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)


class Menu:
 
    def __init__(self, opciones):
        self.opciones = []
        fuente = pygame.font.Font('fuentes/Fuente.ttf', 20)
        x = 105
        y = 105
        paridad = 1

        self.cursor = Cursor(x - 30, y, 30)

        for titulo, funcion in opciones:
            self.opciones.append(Opcion(fuente, titulo, x, y, paridad, funcion))
            y += 30
            if paridad == 1:
                paridad = -1
            else:
                paridad = 1

        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def actualizar(self):
        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.seleccionado -= 1
            elif k[K_DOWN]:
                self.seleccionado += 1
            elif k[K_RETURN]:
                # Invoca a la función asociada a la opción.
                self.opciones[self.seleccionado].activar()

        # procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1
        
        self.cursor.seleccionar(self.seleccionado)

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]

        self.cursor.actualizar()
     
        for o in self.opciones:
            o.actualizar()

    def imprimir(self, screen):
        self.cursor.imprimir(screen)

        for opcion in self.opciones:
            opcion.imprimir(screen)

def comenzar_nuevo_juego():        
    game.run()

def mostrar_opciones():
    a = Image.open("data.png", "r")
    b = Image.open("compare.png", "r")
    c = Image.open("pie.png", "r")
    file = open("real.txt", "r")
    a.show()
    b.show()
    c.show()
    file.close()

def salir_del_programa():
    pygame.quit()

def menu_principal():
    game.menu_inicial.display_menu()
    
class Run_datas():
    def run(self):
        game.menu_inicial.display_menu()
        comenzar_nuevo_juego()
        salir = False
        opciones = [
            ("Repetir simulacion", comenzar_nuevo_juego),
            ("Mostrar graficas", mostrar_opciones),
            ("Salir", salir_del_programa)
            ]

        pygame.font.init()
        screen = pygame.display.set_mode([800, 800])
        fondo = pygame.image.load("fondo.png").convert()
        menu = Menu(opciones)

        while not salir:
            
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    salir = True
                    pygame.quit()
                
            
            screen.blit(fondo, (0,0))
            menu.actualizar()
            menu.imprimir(screen)
            pygame.display.flip()
            pygame.time.delay(10)
        pygame.quit()
