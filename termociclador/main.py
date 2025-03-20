# main.py

import tkinter as tk
from ui import abrir_puerto, archivo, abrir_archivo, editar_archivo, play


# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Termociclador")
ventana.state("zoomed")
ventana.configure(bg="#4682B4")

frame_principal = tk.Frame(ventana, bg="#4682B4")
frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

botones_frame = tk.Frame(frame_principal, bg="#4682B4")
botones_frame.pack()

# Botones
tk.Button(botones_frame, text="Abrir Puerto", command=abrir_puerto, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Nuevo Archivo", command=archivo, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Abrir Archivo", command=abrir_archivo, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Play", command=play, bg="white", fg="black", width=20).pack(pady=10)
tk.Button(botones_frame, text="Editar Archivo", command=editar_archivo, bg="white", fg="black", width=20).pack(pady=10)

# Área para mostrar los datos que se enviarán
datos_label = tk.Label(frame_principal, text="Datos a Enviar:", bg="#4682B4", fg="white", anchor="w", justify="left")
datos_label.pack(pady=20)

ventana.mainloop()
