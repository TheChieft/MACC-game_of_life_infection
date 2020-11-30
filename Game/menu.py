#FINAL_CODE
import os
import pygame
from PIL import Image
class Menu():
    def __init__(self,game):
        self.game=game #usar modulo del juego
        self.mid_w, self.mid_h = self.game.screen_w/2 , self.game.screen_h/2 #mitad de la pantalla
        self.run_menu =True #EL estado del menu. Si esta corriendo o no
        self.cursor_rect=pygame.Rect(0,0,20,20) #dimenciones del RECT del cursos
        self.offset =-100 #distancia del RECT al "cursos" 

    def draw_cursor(self): #DIBUJAR EL CURSOR
        self.game.draw_text('>', 20, self.cursor_rect.x, self.cursor_rect.y) 

    def blit_screen(self): #actualizar pantalla y perifericos 
        self.game.screen.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class Menu_screen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.titlex, self.titley = self.mid_w, self.mid_h +30
        self.reglasx, self.reglasy = self.mid_w, self.mid_h + 60
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.titlex + self.offset, self.titley)

    def display_menu(self):
        self.run_menu = True
        while self.run_menu:
            self.game.events() #Eventos del teclado y mouse
            self.check_input() #revisar la seleccion
            self.game.display.fill(self.game.negro)
            self.game.draw_text("GAME OF LIFE:", 60, self.game.screen_w / 2, self.game.screen_h / 2 -90) #DIBUJAR TITULO PANTALLA
            self.game.draw_text("infection", 45, self.game.screen_w / 2, self.game.screen_h / 2 - 40) #DIBUJAR TITULO PANTALLA
            self.game.draw_text("Juego", 30, self.titlex, self.titley) #DIBUJAR "botones" pantalla
            self.game.draw_text("Reglas", 30, self.reglasx, self.reglasy) #DIBUJAR "botones" pantalla
            self.game.draw_text("Exit", 30, self.exitx, self.exity) #DIBUJAR "botones" pantalla
            self.draw_cursor() #dibujar el cursor con sus cordenadas
            self.blit_screen() #actualizar pantalla


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.reglasx + self.offset, self.reglasy)
                self.state = 'Reglas'
            elif self.state == 'Reglas':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.titlex + self.offset, self.titley)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.reglasx + self.offset, self.reglasy)
                self.state = 'Reglas'
            elif self.state == 'Reglas':
                self.cursor_rect.midtop = (self.titlex + self.offset, self.titley)
                self.state = 'Start'
            

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Reglas':
                a=Image.open('Game\REGLAS.png',"r")
                a.show()
            elif self.state == 'Exit':
                self.salir()
            self.run_menu= False

    def salir(self):
        self.game.running = False

    