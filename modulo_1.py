# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 22:32:23 2020

@author: Ana Karina Pulido
"""

import pandas as pd
import matplotlib.pyplot as plt


def dataframe(lista, lista_names):
        df = pd.Series(lista, index = lista_names) #Crea una serie con pandas, la cual permite asociar un valor con un indice para posteriormente organizar la informacion en una tabla.
        print(df)
        


def lista(blancos, rojos, total, segundos): #Se reciben los datos de la simulacion 
    lista = [segundos, blancos, rojos, total ] #se ingresan los datos en una lista para manipularlos despues.
    return lista 


def letalidad(muertos, total):
    letalidad  = muertos / total #se estima la letalidad del virus en la poblacion
    return letalidad 
    

def progreso(lista, y): #funcion para conocer el progreso del virus en la poblacion
    segundos = lista[0] 
    for i in range(segundos):
        df = pd.Series(i, index = y)
        print(df)
    
    
def porcentajes(df): #Se crean porcentajes de infectados y no infectados 
    lista = []
    porcentaje_infectados = (df[2] / df[3])*100
    lista.append(porcentaje_infectados)
    porcentaje_sin_cont = (df[1] / df[3])*100
    lista.append(porcentaje_sin_cont)
    return lista

def pie_graph(porcentajes): #Funcion que crea una grafica tipo pie para infectados y no infectados con los porcentajes que se ingresan

    labels = 'Infectados', 'No infectados'
    sizes = porcentajes
    explode = (0.1, 0)  #Resalta una parte de la grafica 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  
    plt.show()
    

       
   
#PRUEBA--------------------------------------------------------------

"""x = lista(89, 98, 190, 23)
dataframe(x, ['Segundos', 'Blancos', 'Rojas', 'Total'])
z = porcentajes(x)
w = pie_graph(z)
progreso(x, [1, 2, 3, 4, 5, 6, 7, 10, 12])"""
