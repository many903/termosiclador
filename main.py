import tkinter as tk
from tkinter import messagebox, filedialog
import serial
import serial.tools.list_ports
import os
import math

# Variables globales
ser = None
datos_cargados = {}
entradas = {}
filename = None  # Variable global para almacenar el nombre del archivo cargado

def abrir_puerto():
    """Muestra los puertos serie disponibles y permite al usuario seleccionar uno para conectarse."""
    global ser
    puertos_disponibles = [port.device for port in serial.tools.list_ports.comports()]
    
    if not puertos_disponibles:
        messagebox.showerror("Error", "No se encontraron puertos disponibles.")
        return
    
    ventana_puerto = tk.Toplevel()
    ventana_puerto.title("Seleccionar Puerto")
    ventana_puerto.geometry("300x200")
    
    tk.Label(ventana_puerto, text="Seleccione el puerto:").pack(pady=10)
    puerto_var = tk.StringVar(value=puertos_disponibles[0])
    lista_puertos = tk.OptionMenu(ventana_puerto, puerto_var, *puertos_disponibles)
    lista_puertos.pack(pady=10)
    
    def conectar():
        """Intenta conectar al puerto seleccionado."""
        global ser
        try:
            ser = serial.Serial(puerto_var.get(), baudrate=9600, timeout=1)
            messagebox.showinfo("Éxito", f"Conectado a {puerto_var.get()}")
            ventana_puerto.destroy()
        except serial.SerialException:
            messagebox.showerror("Error", "No se pudo abrir el puerto seleccionado.")
    
    tk.Button(ventana_puerto, text="Conectar", command=conectar).pack(pady=10)

def enviar_datos(comando):
    """Envía un comando por el puerto serie."""
    if ser:
        ser.write(comando.encode())
        print(f"Enviado: {comando}")
    else:
        print("Error: No hay conexión con el puerto serie.")

def play():
    """Ejecuta el cálculo del ciclo y envía los datos."""
    try:
        vuelta = int(entradas["numCiclos"].get())
        resultado = math.factorial(vuelta)
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

    tk.Label(menu_arch, text="Ciclo (Contenido a enviar)", bg="#4682B4", fg="white").pack(anchor=tk.NW)
    ciclo_texto = tk.Text(menu_arch, height=5, width=40)
    ciclo_texto.pack(pady=10)

    tk.Button(menu_arch, text="Guardar", command=lambda: guardar_datos(menu_arch)).pack(pady=10)
    tk.Button(menu_arch, text="Enviar por Puerto Serie", command=enviar_por_puerto).pack(pady=10)

def guardar_datos(ventana):
    datos = {etiqueta: entradas[etiqueta].get() for etiqueta in entradas}
    datos["ciclo"] = ciclo_texto.get("1.0", tk.END).strip()
    
    global filename
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        with open(filename, "w") as file:
            for key, value in datos.items():
                file.write(f"{key}: {value}\n")
        messagebox.showinfo("Guardado", "Datos guardados exitosamente.")

def abrir_archivo():
    """Abre y carga datos desde un archivo guardado."""
    global datos_cargados, filename
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        with open(filename, "r") as file:
            datos_cargados.clear()
            for line in file:
                clave, valor = line.strip().split(": ", 1)
                datos_cargados[clave] = valor
        messagebox.showinfo("Cargado", "Datos cargados exitosamente.")
        actualizar_campos()

def actualizar_campos():
    """Llena los campos con los datos cargados."""
    for key, entry in entradas.items():
        if key in datos_cargados:
            entry.delete(0, tk.END)
            entry.insert(0, datos_cargados[key])
    ciclo_texto.delete("1.0", tk.END)
    if "ciclo" in datos_cargados:
        ciclo_texto.insert("1.0", datos_cargados["ciclo"])

def editar_archivo():
    """Permite editar un archivo previamente cargado."""
    global datos_cargados
    if not datos_cargados:
        messagebox.showerror("Error", "No hay datos cargados para editar.")
        return

    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Archivo")
    
    tk.Label(ventana_edicion, text="Editar Datos del Archivo").pack(pady=10)
    
    # Crear campos de edición basados en los datos cargados
    for key, value in datos_cargados.items():
        tk.Label(ventana_edicion, text=key).pack(pady=5)
        entry = tk.Entry(ventana_edicion)
        entry.insert(0, value)
        entry.pack(pady=5)
        entradas[key] = entry
    
    def guardar_ediciones():
        """Guardar los datos editados en el archivo original."""
        datos_editados = {key: entry.get() for key, entry in entradas.items()}
        
        global filename
        if not filename:
            filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        
        if filename:
            with open(filename, "w") as file:
                for key, value in datos_editados.items():
                    file.write(f"{key}: {value}\n")
            messagebox.showinfo("Guardado", "Datos editados y guardados exitosamente.")
            ventana_edicion.destroy()

    tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_ediciones).pack(pady=10)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Termociclador")
ventana.state("zoomed")
ventana.configure(bg="#4682B4")

frame_principal = tk.Frame(ventana, bg="#4682B4")
frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

botones_frame = tk.Frame(frame_principal, bg="#4682B4")
botones_frame.pack()

tk.Button(botones_frame, text="Abrir Puerto", command=abrir_puerto, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Nuevo Archivo", command=guardar_datos, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Abrir Archivo", command=abrir_archivo, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Play", command=play, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Editar Archivo", command=editar_archivo, bg="white", fg="black", width=20).pack(pady=10)

menubar = tk.Menu(ventana)
ventana.config(menu=menubar)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Abrir Puerto", command=abrir_puerto)
filemenu.add_command(label="Nuevo", command=guardar_datos)
filemenu.add_command(label="Abrir", command=abrir_archivo)
filemenu.add_command(label="Editar Archivo", command=editar_archivo)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=ventana.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)

ventana.mainloop()
