import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import serial
import time
import os
import math

# Configuración del puerto serie
try:
    ser = serial.Serial("COM3", baudrate=9600, timeout=1)  # Ajusta el puerto según tu configuración
except serial.SerialException:
    ser = None
    print("Error: No se pudo abrir el puerto serie.")

# Funciones

def enviar_datos(comando):
    if ser:
        ser.write(comando.encode())
        print(f"Enviado: {comando}")
    else:
        print("Error: No hay conexión con el puerto serie.")

def calcular_exponencial(vuelta):
    return math.factorial(vuelta)

def play():
    try:
        vuelta = int(vuelta_entry.get())
        resultado = calcular_exponencial(vuelta)
        enviar_datos(f"CICLO:{resultado}")
        print(f"Ciclo {vuelta} calculado: {resultado}")
    except ValueError:
        messagebox.showerror("Error", "Ingrese un valor numérico válido para la vuelta.")

def archivo():
    menu_arch = tk.Toplevel()
    menu_arch.title("Nuevo Archivo")
    menu_arch.geometry("400x500")
    menu_arch.configure(bg="#4682B4")

    global vuelta_entry, ciclo_texto
    tk.Label(menu_arch, text="Número de vuelta", bg="#4682B4", fg="white").pack(anchor=tk.NW)
    vuelta_entry = tk.Entry(menu_arch)
    vuelta_entry.pack()

    # Cuadro de texto para que el usuario ingrese el ciclo
    tk.Label(menu_arch, text="Ciclo (Contenido a enviar)", bg="#4682B4", fg="white").pack(anchor=tk.NW)
    ciclo_texto = tk.Text(menu_arch, height=10, width=40)
    ciclo_texto.pack(pady=10)

    tk.Button(menu_arch, text="Guardar", command=lambda: guardar_datos(menu_arch)).pack(pady=10)
    tk.Button(menu_arch, text="Enviar por Puerto Serie", command=enviar_por_puerto).pack(pady=10)

def guardar_datos(ventana):
    # Obtiene el contenido del cuadro de texto
    datos = {"vuelta": vuelta_entry.get(), "ciclo": ciclo_texto.get("1.0", tk.END).strip()}
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        with open(filename, "w") as file:
            for key, value in datos.items():
                file.write(f"{key}: {value}\n")
        messagebox.showinfo("Guardado", "Datos guardados exitosamente.")
        ventana.destroy()

def enviar_por_puerto():
    ciclo_contenido = ciclo_texto.get("1.0", tk.END).strip()  # Obtiene el contenido del ciclo
    if ciclo_contenido:
        enviar_datos(ciclo_contenido)  # Enviar el contenido del ciclo por puerto serie
        messagebox.showinfo("Enviado", "Ciclo enviado por puerto serie.")
    else:
        messagebox.showerror("Error", "El ciclo está vacío, ingrese contenido antes de enviarlo.")

def abrir_archivo():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        os.system(f"notepad {filename}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Termociclador")
ventana.state("zoomed")  # Ajustar la ventana al tamaño de la pantalla
ventana.configure(bg="#4682B4")

# Frame principal para diseño organizado
frame_principal = tk.Frame(ventana, bg="#4682B4")
frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Espacio para imágenes decorativas
imagen_frame = tk.Frame(frame_principal, bg="#4682B4")
imagen_frame.pack(pady=20)

# Contenedor de botones
botones_frame = tk.Frame(frame_principal, bg="#4682B4")
botones_frame.pack()

# Botones principales
tk.Button(botones_frame, text="Programa Nuevo", bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Play", command=play, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Pausa", bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Nuevo Archivo", command=archivo, bg="white", fg="black", width=20).pack(pady=10)

# Menú
menubar = tk.Menu(ventana)
ventana.config(menu=menubar)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Nuevo", command=archivo)
filemenu.add_command(label="Abrir", command=abrir_archivo)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=ventana.quit)

menubar.add_cascade(label="Archivo", menu=filemenu)

# Ejecutar la interfaz
ventana.mainloop()
