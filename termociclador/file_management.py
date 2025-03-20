def guardar_datos(filename, datos):
    if filename:
        with open(filename, "w") as file:
            for key, value in datos.items():
                file.write(f"{key}: {value}\n")
        return True
    return False

def cargar_datos(filename):
    datos_cargados = {}
    if filename:
        with open(filename, "r") as file:
            for line in file:
                clave, valor = line.strip().split(": ", 1)
                datos_cargados[clave] = valor
    return datos_cargados
