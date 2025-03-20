# gestiones_de_error.py

import tkinter as tk
from tkinter import messagebox
import serial

def verificar_puerto(ser):
    """Verifica si el puerto serie está conectado."""
    if not ser or not ser.is_open:
        messagebox.showerror("Error", "No hay conexión con el puerto serie.")
        return False
    return True

def verificar_entrada(entrada, nombre):
    """Verifica si la entrada es válida."""
    if not entrada:
        messagebox.showerror("Error", f"El campo '{nombre}' no puede estar vacío.")
        return False
    return True

def verificar_archivo(filename):
    """Verifica si el archivo es válido."""
    if not filename:
        messagebox.showerror("Error", "No se seleccionó un archivo.")
        return False
    return True

def manejar_error_guardado(errores):
    """Manejo de errores al guardar el archivo."""
    if errores:
        messagebox.showerror("Error", "Hubo un problema al guardar el archivo.")
