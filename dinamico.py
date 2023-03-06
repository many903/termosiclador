from tkinter import *
from tkinter import ttk
import tkinter as tk
from webbrowser import * 

lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):

    x, y = event.x - lastClickX + ventana.winfo_x(), event.y - lastClickY + ventana.winfo_y()
    ventana.geometry("+%s+%s" % (x , y))
def track_change_to_text(event):
    text_box.tag_add("here", "1.0", "1.4")
    text_box.tag_config("here", background="black", foreground="green")
def OnMotion(ventana, event):
    x1 = ventana.winfo_pointerx()
    y1 = ventana.winfo_pointery()
    x0 = ventana.winfo_rootx()
    y0 = ventana.winfo_rooty()
    ventana.geometry("%sx%s" % ((x1-x0),(y1-y0)))




ventana = Tk() 



ventana.resizable(height = 0, width = 0)
ventana['bg']='black'
message="9"
ventana.resizable(True, True)
ventana.grip = ttk.Sizegrip(ventana)
ventana.grip.place(relx=1.0, rely=1.0, anchor="se")

ventana.grip.bind("<B1-Motion>", lambda event:OnMotion(ventana,event))
text_box = Text(ventana,bg="black", bd=0,fg="green",highlightthickness = 0, borderwidth=0)
text_box.pack()
text_box.bind('<KeyPress>', track_change_to_text)
 
ventana.mainloop()