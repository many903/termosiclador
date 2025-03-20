# main.py

import tkinter as tk
from tkinter import messagebox
from ui import abrir_puerto, play, archivo, abrir_archivo, editar_archivo

def iniciar_ventana_principal():
    """Crea la ventana principal de la interfaz de usuario."""
    ventana = tk.Tk()
    ventana.title("Control del Termosiclador")
    ventana.geometry("600x400")
    ventana.configure(bg="#4682B4")

    # Etiqueta de bienvenida
    tk.Label(ventana, text="Bienvenido al control del Termosiclador", bg="#4682B4", fg="white", font=("Helvetica", 16)).pack(pady=20)

    # Botón para abrir la ventana de puerto
    tk.Button(ventana, text="Abrir Puerto", command=abrir_puerto, width=20).pack(pady=10)

    # Botón para iniciar el ciclo
    tk.Button(ventana, text="Iniciar Ciclo", command=play, width=20).pack(pady=10)

    # Botón para crear nuevo archivo de datos
    tk.Button(ventana, text="Nuevo Archivo", command=archivo, width=20).pack(pady=10)

    # Botón para abrir archivo existente
    tk.Button(ventana, text="Abrir Archivo", command=abrir_archivo, width=20).pack(pady=10)

    # Botón para editar archivo existente
    tk.Button(ventana, text="Editar Archivo", command=editar_archivo, width=20).pack(pady=10)

    # Ejecutar la ventana
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_ventana_principal()
