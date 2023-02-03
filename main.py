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

#ajuste y personalizacion de la ventana
boton = tk.Button(text="Boton")
boton.place(x=50, y=50)

ventana.mainloop()#se mantiene la vantana este simpre tiene que estar al final de la config. de la ventana

