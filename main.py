# que librerias necesito si quiero un porgrama el cual me abra un ventana con ciertos criterios que me permitan lleva a cavo una interface 
# y esta interafas al mismo tiempo me permita manajar uun dispocitivio por puerto seria
# dentro de este dispocitivo nececito manejar:
#  ventiladores ,sensro de temperatura, relay, 3 leds(cada led con su funcion correspondiente) y un buzzer 

#librerias
import tkinter as tk
from tkinter import *
import serial
import time

#variables predeterminadas 
a = 1920
b = 1080 

#funciones del programa
#funcion del boton play
def play():
    if preca==0:
        print("error de variable ")    
    else:
        print("precalentamiento establecido")
        #activa el puerto serial y envia la variable preca 

#boton de la funcion de nuevo archivo
def archivo ():
    messgebox.showinfo(message = "incerte las variables del nuevo programa",title = "nuevo archivo")

#ajustes de la ventana
ventana = Tk()
ventana.title ("termociclador") #nombre de la ventana
ventana.geometry("1920x1080") #tamaño de la vendatana
#ventana.iconbitmap("form.ico") #Cambiar el icono no hasta escojer un icono 
ventana.config(bg="blue")#color de la ventana
#ajuste y personalizacion de la ventana del sistema 
#boton de play
boton = tk.Button(text="play")
boton.place(x = a-100, y = b-1000)

#boton de pausa
botonII = tk.Button(text="puase",command = play)
botonII.place(x = a-150, y = b-1000)

#boton para agregar un nuevo archivo
new = tk.Button(text="nuevo archivo",command = archivo)
new.place(x = a-600, y = b-1000)

ventana.mainloop()#se mantiene la vantana este simpre tiene que estar al final de la config. de la ventana

#funciones del programa
#funcion del boton play
#def play():
    


#funcion del boton pause
#def pausa():

#que se tiene que enviar una vez se da en el boton de start
def play():
    if preca==0:
        print("error de variable ")    
    else:
        print("precalentamiento establecido")
        #activa el puerto serial y envia la variable preca 

#def repeticion():
    
    

#variables de tiempo y temperatura 
preca = int(input(" la temperatura de precalentado :"))
time1 =int (input("tiempo 1"))
time2 =int (input("tiempo 1"))
time3 =int (input("tiempo 1"))
time4 =int (input("tiempo 1"))
enfriamiento =int (input("tiempo 1"))
temp1 = int (input("temperatura de precalentado"))
temp2 = int (input("temperatura"))
temp3 = int (input("temperatura"))
temp4 = int (input("temperatura"))
temp5 = int (input("temperatura"))
