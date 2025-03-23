import tkinter as tk
from tkinter import messagebox, filedialog
import serial
import serial.tools.list_ports
import math

# Variables globales
ser = None
datos_cargados = {}
entradas = {}
filename = None
ciclo_texto = None

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

def calcular_factorial(vuelta):
    """Calcula el factorial de vuelta (vuelta!)."""
    return math.factorial(vuelta)

def play():
    """Ejecuta el cálculo del ciclo, muestra los datos y los envía."""
    try:
        vuelta = int(entradas["numCiclos"].get())
        resultado = calcular_factorial(vuelta)
        datos = {key: entradas[key].get() for key in entradas}
        datos["ciclo"] = ciclo_texto.get("1.0", tk.END).strip()
        datos["resultado_factorial"] = resultado
        datos_label.config(text=f"Datos a Enviar:\n{datos}")
        enviar_datos(f"Factorial:{resultado}")
    except ValueError:
        messagebox.showerror("Error", "Ingrese un valor numérico válido para la vuelta.")

def archivo_nuevo():
    """Crea una nueva ventana para ingresar datos y guarda esos datos en un archivo."""
    global ciclo_texto, entradas, filename
    entradas = {}
    menu_arch = tk.Toplevel()
    menu_arch.title("Nuevo Archivo")
    menu_arch.geometry("400x600")

    etiquetas = [
        ("Temperatura Inicial", "tempInicial"),
        ("Temperatura Máxima", "tempMax"),
        ("Temperatura Media", "tempMed"),
        ("Temperatura Mínima", "tempMin"),
        ("Tiempo 1", "time1"),
        ("Tiempo 2", "time2"),
        ("Tiempo 3", "time3"),
        ("Número de Ciclos", "numCiclos"),
    ]

    for etiqueta, key in etiquetas:
        frame = tk.Frame(menu_arch)
        frame.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(frame, text=etiqueta, width=25, anchor='w').pack(side=tk.LEFT)
        entrada = tk.Entry(frame)
        entrada.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        entradas[key] = entrada

    tk.Label(menu_arch, text="Ciclo").pack()
    ciclo_texto = tk.Text(menu_arch, height=5, width=40)
    ciclo_texto.pack(pady=10)
    tk.Button(menu_arch, text="Guardar", command=guardar_datos).pack(pady=10)

def guardar_datos():
    """Guarda los datos del archivo nuevo o abierto."""
    global filename
    datos = {key: entradas[key].get() for key in entradas}
    datos["ciclo"] = ciclo_texto.get("1.0", tk.END).strip()
    
    if filename:  # Si ya se abrió un archivo, guarda en el mismo archivo
        with open(filename, "w") as file:
            for key, value in datos.items():
                file.write(f"{key}: {value}\n")
        messagebox.showinfo("Guardado", "Datos guardados exitosamente.")
        actualizar_nombre_archivo()
    else:  # Si no hay un archivo cargado, se pide al usuario uno nuevo
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            with open(filename, "w") as file:
                for key, value in datos.items():
                    file.write(f"{key}: {value}\n")
            messagebox.showinfo("Guardado", "Datos guardados exitosamente.")
            actualizar_nombre_archivo()

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
    global entradas
    for key, entry in entradas.items():
        if key in datos_cargados:
            entry.delete(0, tk.END)
            entry.insert(0, datos_cargados[key])
    ciclo_texto.delete("1.0", tk.END)
    if "ciclo" in datos_cargados:
        ciclo_texto.insert("1.0", datos_cargados["ciclo"])

def habilitar_edicion():
    """Habilita los campos de entrada y el texto para editar."""
    global entradas, ciclo_texto
    for key, entry in entradas.items():
        entry.config(state=tk.NORMAL)  # Habilita el campo de entrada
    ciclo_texto.config(state=tk.NORMAL)  # Habilita el campo de texto

def deshabilitar_edicion():
    """Deshabilita los campos de entrada y el texto para evitar cambios."""
    global entradas, ciclo_texto
    for key, entry in entradas.items():
        entry.config(state=tk.DISABLED)  # Deshabilita el campo de entrada
    ciclo_texto.config(state=tk.DISABLED)  # Deshabilita el campo de texto

def actualizar_nombre_archivo():
    """Actualiza la etiqueta con el nombre del archivo cargado o guardado."""
    if filename:
        nombre_archivo = filename.split("/")[-1]  # Extrae solo el nombre del archivo
        datos_label.config(text=f"Archivo: {nombre_archivo}")
    else:
        datos_label.config(text="Datos a Enviar:")

root = tk.Tk()
root.title("Interfaz Termociclador")
root.geometry("500x400")

# Barra de menú
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
menu_archivo = tk.Menu(menu_bar, tearoff=0)
menu_archivo.add_command(label="Nuevo", command=archivo_nuevo)
menu_archivo.add_command(label="Abrir", command=abrir_archivo)
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)
menu_bar.add_command(label="Abrir Puerto", command=abrir_puerto)
menu_bar.add_command(label="Ejecutar", command=play)

# Botones en la pantalla
frame_boton = tk.Frame(root)
frame_boton.pack(pady=10)

btn_nuevo = tk.Button(frame_boton, text="Nuevo", command=archivo_nuevo)
btn_nuevo.pack(side=tk.LEFT, padx=5)

btn_abrir = tk.Button(frame_boton, text="Abrir Archivo", command=abrir_archivo)
btn_abrir.pack(side=tk.LEFT, padx=5)

btn_abrir_puerto = tk.Button(frame_boton, text="Abrir Puerto", command=abrir_puerto)
btn_abrir_puerto.pack(side=tk.LEFT, padx=5)

btn_ejecutar = tk.Button(frame_boton, text="Ejecutar", command=play)
btn_ejecutar.pack(side=tk.LEFT, padx=5)

# Label para mostrar el nombre del archivo cargado o guardado
datos_label = tk.Label(root, text="Datos a Enviar:")
datos_label.pack(pady=20)

root.mainloop()
