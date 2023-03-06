# que librerias necesito si quiero un porgrama el cual me abra un ventana con ciertos criterios que me permitan lleva a cavo una interface 
# y esta interafas al mismo tiempo me permita manajar uun dispocitivio por puerto seria
# dentro de este dispocitivo nececito manejar:
#  ventiladores ,sensro de temperatura, relay, 3 leds(cada led con su funcion correspondiente) y un buzzer 

#librerias
import tkinter as tk
from tkinter import *
from tkinter import messagebox as MessageBox
from tkinter import ttk
#import serial
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
    menu_arch = Tk()
    menu_arch.title("Archivo nuevo")
    menu_arch.geometry("200x200")
    Label(menu_arch,title="temperatura de precalentameinto").pack(anchor=NW)
    preca = Entry(menu_arch)
    preca.pack()
    Label(menu_arch,title="temperatura de precalentameinto").pack(anchor=NW)
    temp1 = Entry(menu_arch)
    temp1.pack()
    Label(menu_arch,title="temperatura de precalentameinto").pack(anchor=NW)
    temp2 = Entry(menu_arch)
    temp2.pack()
    Label(menu_arch,title="temperatura de precalentameinto").pack(anchor=NW)
    temp3 = Entry(menu_arch)
    temp3.pack()
    Label(menu_arch,title="temperatura de precalentameinto").pack(anchor=NW)
    temp4 = Entry(menu_arch)
    temp4.pack()
    Label(menu_arch,title="temperatura de precalentameinto").pack(anchor=NW)
    temp5 = Entry(menu_arch)
    temp5.pack()




#ajustes de la ventana
ventana = Tk()
ventana.title ("termociclador") #nombre de la ventana
ventana.geometry("1920x1080") #tamaño de la vendatana
#ventana.iconbitmap("form.ico") #Cambiar el icono no hasta escojer un icono 
ventana.config(bg="black")#color de la ventana
#ajuste y personalizacion de la ventana del sistema 
#boton de play
boton = tk.Button(text="play")
boton.place(x = a-100, y = b-1000)

#barra de menu
menubar = Menu(ventana)
ventana.config(menu = menubar)
filemenu = Menu(ventana)
editmenu = Menu(ventana)
helpmenu = Menu(ventana)

#menu sub-clases
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Nuevo",command="archivo")
filemenu.add_command(label="Abrir")
filemenu.add_command(label="Guardar")
filemenu.add_command(label="Cerrar")
editmenu = Menu(menubar, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)

#añadidos al menu
menubar.add_cascade(label="Archivo", menu=filemenu)
menubar.add_cascade(label="Editar", menu=editmenu)
menubar.add_cascade(label="Ayuda", menu=helpmenu)

#cierre de la ventana
filemenu.add_separator()
filemenu.add_command(label="Salir", command=ventana.quit)
#boton de pausa
botonII = tk.Button(text="puase",command = play)
botonII.place(x = a-150, y = b-1000)

#boton para agregar un nuevo archivo
new = tk.Button(text="nuevo archivo",command = archivo)
new.place(x = a-600, y = b-1000)

#mainloop

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
time2 =int (input("tiempo 2"))
time3 =int (input("tiempo 3"))
time4 =int (input("tiempo 4"))
enfriamiento =int (input("tiempo 4"))
temp1 = int (input("temperatura de precalentado"))
temp2 = int (input("temperatura"))
temp3 = int (input("temperatura"))
temp4 = int (input("temperatura"))
temp5 = int (input("temperatura"))
