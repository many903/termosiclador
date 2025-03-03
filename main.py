import tkinter as tk
from tkinter import messagebox, filedialog
import serial
import os
import math

# Configuración del puerto serie
try:
    ser = serial.Serial("COM3", baudrate=9600, timeout=1)
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
    menu_arch.geometry("400x600")
    menu_arch.configure(bg="#4682B4")

    global vuelta_entry, ciclo_texto, entradas
    entradas = {}
    etiquetas = [
        ("Temperatura Inicial", "tempInicial"),
        ("Temperatura Máxima", "tempMax"),
        ("Temperatura Media", "tempMed"),
        ("Temperatura Mínima", "tempMin"),
        ("Temperatura de Almacenamiento", "tempAlm"),
        ("Tiempo 1", "time1"),
        ("Tiempo 2", "time2"),
        ("Tiempo 3", "time3"),
        ("Tiempo 4", "time4"),
        ("Número de Ciclos", "numCiclos")
    ]

    for etiqueta, key in etiquetas:
        frame = tk.Frame(menu_arch, bg="#4682B4")
        frame.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(frame, text=etiqueta, bg="#4682B4", fg="white", width=25, anchor='w').pack(side=tk.LEFT)
        entrada = tk.Entry(frame)
        entrada.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        entradas[key] = entrada

    # Cuadro de texto para el ciclo
    tk.Label(menu_arch, text="Ciclo (Contenido a enviar)", bg="#4682B4", fg="white").pack(anchor=tk.NW)
    ciclo_texto = tk.Text(menu_arch, height=5, width=40)
    ciclo_texto.pack(pady=10)

    tk.Button(menu_arch, text="Guardar", command=lambda: guardar_datos(menu_arch)).pack(pady=10)
    tk.Button(menu_arch, text="Enviar por Puerto Serie", command=enviar_por_puerto).pack(pady=10)

def guardar_datos(ventana):
    datos = {etiqueta: entradas[etiqueta].get() for etiqueta in entradas}
    datos["ciclo"] = ciclo_texto.get("1.0", tk.END).strip()
    
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        with open(filename, "w") as file:
            for key, value in datos.items():
                file.write(f"{key}: {value}\n")
            file.write("orden: " + ",".join([datos[key] for key in entradas]) + "\n")
        messagebox.showinfo("Guardado", "Datos guardados exitosamente.")
        ventana.destroy()

def enviar_por_puerto():
    datos = {etiqueta: entradas[etiqueta].get() for etiqueta in entradas}
    datos["ciclo"] = ciclo_texto.get("1.0", tk.END).strip()
    comando = "orden: " + ",".join([datos[key] for key in entradas])
    enviar_datos(comando)
    messagebox.showinfo("Enviado", "Datos enviados por puerto serie.")

def abrir_archivo():<<
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        os.system(f"notepad {filename}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Termociclador")
ventana.state("zoomed")
ventana.configure(bg="#4682B4")

frame_principal = tk.Frame(ventana, bg="#4682B4")
frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

botones_frame = tk.Frame(frame_principal, bg="#4682B4")
botones_frame.pack()

tk.Button(botones_frame, text="Nuevo Archivo", command=archivo, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Play", command=play, bg="white", fg="black", width=20).pack(pady=10)

menubar = tk.Menu(ventana)
ventana.config(menu=menubar)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Nuevo", command=archivo)
filemenu.add_command(label="Abrir", command=abrir_archivo)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=ventana.quit)

menubar.add_cascade(label="Archivo", menu=filemenu)

ventana.mainloop()
