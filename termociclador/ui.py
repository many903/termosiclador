import tkinter as tk
from tkinter import messagebox, filedialog
from termociclador.serial_port import abrir_puerto, conectar_puerto, enviar_datos
from file_management import guardar_datos, cargar_datos

class TermocicladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Termociclador")
        self.root.state("zoomed")
        self.root.configure(bg="#4682B4")

        self.frame_principal = tk.Frame(self.root, bg="#4682B4")
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.entradas = {}
        self.filename = None
        self.datos_cargados = {}

        self.configurar_botones()

    def configurar_botones(self):
        botones_frame = tk.Frame(self.frame_principal, bg="#4682B4")
        botones_frame.pack()

        tk.Button(botones_frame, text="Abrir Puerto", command=self.abrir_puerto, bg="white", fg="black", width=20).pack(pady=10)
        tk.Button(botones_frame, text="Nuevo Archivo", command=self.abrir_archivo, bg="white", fg="black", width=20).pack(pady=10)
        tk.Button(botones_frame, text="Abrir Archivo", command=self.abrir_archivo, bg="white", fg="black", width=20).pack(pady=10)
        tk.Button(botones_frame, text="Play", command=self.play, bg="white", fg="black", width=20).pack(pady=10)
        tk.Button(botones_frame, text="Editar Archivo", command=self.editar_archivo, bg="white", fg="black", width=20).pack(pady=10)

        self.datos_label = tk.Label(self.frame_principal, text="Datos a Enviar:", bg="#4682B4", fg="white", anchor="w", justify="left")
        self.datos_label.pack(pady=20)

    def abrir_puerto(self):
        puertos_disponibles, error = abrir_puerto()
        if error:
            messagebox.showerror("Error", error)
            return

        ventana_puerto = tk.Toplevel(self.root)
        ventana_puerto.title("Seleccionar Puerto")
        ventana_puerto.geometry("300x200")

        tk.Label(ventana_puerto, text="Seleccione el puerto:").pack(pady=10)
        puerto_var = tk.StringVar(value=puertos_disponibles[0])
        lista_puertos = tk.OptionMenu(ventana_puerto, puerto_var, *puertos_disponibles)
        lista_puertos.pack(pady=10)

        def conectar():
            exito, mensaje = conectar_puerto(puerto_var.get())
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana_puerto.destroy()
            else:
                messagebox.showerror("Error", mensaje)

        tk.Button(ventana_puerto, text="Conectar", command=conectar).pack(pady=10)

    def play(self):
        try:
            if "numCiclos" not in self.entradas:
                messagebox.showerror("Error", "'Número de Ciclos' no está disponible.")
                return

            vuelta = int(self.entradas["numCiclos"].get())
            # Aquí va la lógica para calcular el ciclo, enviar los datos, etc.

        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido para la vuelta.")

    def abrir_archivo(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filename:
            self.datos_cargados = cargar_datos(self.filename)
            messagebox.showinfo("Cargado", "Datos cargados exitosamente.")
            self.actualizar_campos()

    def actualizar_campos(self):
        for key, entry in self.entradas.items():
            if key in self.datos_cargados:
                entry.delete(0, tk.END)
                entry.insert(0, self.datos_cargados[key])

    def editar_archivo(self):
        if not self.datos_cargados:
            messagebox.showerror("Error", "No hay datos cargados para editar.")
            return

        ventana_edicion = tk.Toplevel(self.root)
        ventana_edicion.title("Editar Archivo")

        tk.Label(ventana_edicion, text="Editar Datos del Archivo").pack(pady=10)

        for key, value in self.datos_cargados.items():
            tk.Label(ventana_edicion, text=key).pack(pady=5)
            entry = tk.Entry(ventana_edicion)
            entry.insert(0, value)
            entry.pack(pady=5)
            self.entradas[key] = entry

        def guardar_ediciones():
            datos_editados = {key: entry.get() for key, entry in self.entradas.items()}
            if guardar_datos(self.filename, datos_editados):
                messagebox.showinfo("Guardado", "Datos editados y guardados exitosamente.")
                ventana_edicion.destroy()

        tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_ediciones).pack(pady=10)

def main():
    ventana = tk.Tk()
    app = TermocicladorApp(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()
