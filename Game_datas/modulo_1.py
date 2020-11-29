# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 22:32:23 2020

@author: Ana Karina Pulido
"""

import pandas as pd
import matplotlib.pyplot as plt

#FUNCION DATAFRAME: Crea una serie con pandas, la cual permite asociar 
#un valor con un indice para posteriormente organizar la informacion en una tabla.
#-------------------------------------------------------------------------------------------------------------------------------------------------
def dataframe(lista, lista_names):
        df = pd.Series(lista, index = lista_names) 
        return df
#------------------------------------------------------------------------------------------------------------------------------------------------    
    
#FUNCION LISTA: Crea una lista con los datos de celulas blancas, rojas y el total.
#---------------------------------------------------------------------------------------------------
def lista(blancos, rojos, total): #Se reciben los datos de la simulacion 
    lista = [blancos, rojos, total ] #se ingresan los datos en una lista para manipularlos despues.
    return lista 
#---------------------------------------------------------------------------------------------------

#FUNCION PORCENTAJES: Se crean porcentajes de infectados y no infectados 
#--------------------------------------------------------------------------------------------------
def porcentajes(df): 
    lista = []
    porcentaje_infectados = (df[1] / df[2])*100
    lista.append(porcentaje_infectados)
    porcentaje_sin_cont = (df[0] / df[2])*100
    lista.append(porcentaje_sin_cont)
    return lista
#---------------------------------------------------------------------------------------------------

#FUNCION PIE-GRAP: crea una grafica tipo pie.
#----------------------------------------------------------------------------------------------
def pie_graph(porcentajes, segundos): #Funcion que crea una grafica tipo pie para infectados 
# y no infectados con los porcentajes que se ingresan

    labels = 'Infectados', 'No infectados' #Se da titulo a las partes de la grafica
    sizes = porcentajes #el tamaño de cada trozo sera los porcentajes ingresados a la funcion
    explode = (0.1, 0)  #Resalta una parte de la grafica 
    
    fig1, ax1 = plt.subplots() 
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  #permite que todos los lados sean proporcionales 
    plt.title(segundos+" segundos transcurridos") #asigna un titulo segun el tiempo transcurrido
    plt.savefig("pie.png") #guarda la grafica en formato png 
    #plt.show()
    plt.clf() #funcion para que la grafica no se sobreponga a la anterior
#-------------------------------------------------------------------------------------------------
    
#FUNCION DATA: Crea una grafica de barras con la informacion de las celulas infectadas
#mostrando cuantas habian en diferentes momentos de la simulacion respecto a la poblacion total.
#-------------------------------------------------------------------------------------------------
def data(x, y, title): 
    plt.barh(x, y, align = 'center', alpha = 0.5) #crea la grafica de barras 
    plt.savefig("data.png")  #guarda la grafica en formato png 
    plt.title(title) #crea un titulo para la grafica
    #plt.show()
    plt.clf()  #funcion para que la grafica no se sobreponga a la anterior
#------------------------------------------------------------------------------------------------------    

#FUNCION COMPARE: funcion que permite crear una grafica donde la informacion se muestra en 
#una sola barra donde se pueden comparar respecto al total de celulas vivas en la simulacion. 
#------------------------------------------------------------------------------------------------------
def compare(total, infectados, poblacion, segundos):
    
    x = total #numero total de celulas 
    y1 = infectados #infectados 
    y2 = poblacion  #poblacion sana o no infectada 
 
    labels = ["Infectados", "Saludables"] #etiquetas de la informacion que sera comparada
    
    fig, ax = plt.subplots() #se crea una figura y un eje en el cual se ubicara la 
    #barra sola para hacer la comparacion de la informacion 
    ax.stackplot(x, y1, y2, labels=labels) #tomando el eje definido anteriormente se agregan 
    #los valores a comparar
    ax.legend(loc='upper left') 
    ax.set_title(str(segundos)+" segundos transcurridos") #se crea un titulo para la grafica con el tiempo transcurrido 
    plt.savefig("compare.png") #guarda la grafica en formato png 
    #plt.show()
    plt.clf() #funcion para que la grafica no se sobreponga a la anterior
#---------------------------------------------------------------------------------------------------------  
    


