from tkinter import *
import tkinter as tk
import ttk
from webbrowser import * 

lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):

    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x , y))
def track_change_to_text(event):
    text_box.tag_add("here", "1.0", "1.4")
    text_box.tag_config("here", background="black", foreground="green")
def OnMotion(window, event):
    x1 = window.winfo_pointerx()
    y1 = window.winfo_pointery()
    x0 = window.winfo_rootx()
    y0 = window.winfo_rooty()
    window.geometry("%sx%s" % ((x1-x0),(y1-y0)))




window = Tk() 



window.resizable(height = 0, width = 0)
window['bg']='black'
message="9"
window.resizable(True, True)
window.grip = ttk.Sizegrip(window)
window.grip.place(relx=1.0, rely=1.0, anchor="se")

window.grip.bind("<B1-Motion>", lambda event:OnMotion(window,event))
text_box = Text(window,bg="black", bd=0,fg="green",highlightthickness = 0, borderwidth=0)
text_box.pack()
text_box.bind('<KeyPress>', track_change_to_text)
 

scrollbar = Scrollbar(window)
t = tk.Text(window, height=10, width=10, yscrollcommand=scrollbar.set)
scrollbar.config(command=t.yview)
scrollbar.pack(side=RIGHT, fill=Y)