# que librerias necesito si quiero un porgrama el cual me abra un ventana con ciertos criterios que me permitan lleva a cavo una interface 
# y esta interafas al mismo tiempo me permita manajar uun dispocitivio por puerto seria
# dentro de este dispocitivo nececito manejar:
#  ventiladores ,sensro de temperatura, relay, 3 leds(cada led con su funcion correspondiente) y un buzzer 

#librerias
import tkinter as tk
from tkinter import *

#ajustes de la ventana
ventana = Tk()
ventana.title ("termociclador") #nombre de la ventana
ventana.geometry("500x500") #tamaño de la venatana
#ventana.iconbitmap("form.ico") #Cambiar el icono no hasta escojer un icono 
ventana.config(bg="gray")#color de la ventana

#ajuste y personalizacion de la ventana del sistema 
#boton de play
boton = tk.Button(text="play")
boton.place(x=450, y=50)

#boton de pausa
botonII = tk.Button(text="puase")
botonII.place(x=400, y=50)

ventana.mainloop()#se mantiene la vantana este simpre tiene que estar al final de la config. de la ventana

#funciones del programa
#funcion del boton play
#def play():
    


#funcion del boton pause
#def pausa():




#main loop
preca = int(input(" la temperatura de precalentado :"))
time1 =
time2 =
time3 =
time4 =
enfriamiento =