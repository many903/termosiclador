from ui import TermocicladorApp

def main():
    # Crear la ventana principal
    import tkinter as tk
    ventana = tk.Tk()

    # Inicializar la aplicación con la ventana
    app = TermocicladorApp(ventana)

    # Iniciar el bucle principal de la interfaz gráfica
    ventana.mainloop()

if __name__ == "__main__":
    main()
