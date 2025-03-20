import serial
import serial.tools.list_ports

ser = None

def abrir_puerto():
    puertos_disponibles = [port.device for port in serial.tools.list_ports.comports()]
    if not puertos_disponibles:
        return None, "No se encontraron puertos disponibles."
    return puertos_disponibles, None

def conectar_puerto(puerto):
    global ser
    try:
        ser = serial.Serial(puerto, baudrate=9600, timeout=1)
        return True, f"Conectado a {puerto}"
    except serial.SerialException:
        return False, "No se pudo abrir el puerto seleccionado."

def enviar_datos(comando):
    if ser:
        ser.write(comando.encode())
        return True
    return False
