/*
  Control de temperatura con Arduino y sensor DS18B20
  
  Requisitos:
  - Placa Arduino compatible
  - Sensor de temperatura DS18B20
  - Puente H para controlar calentamiento y enfriamiento
  - Conexión al puerto serial para enviar comandos
  
  Formato de envío de datos por el puerto serial:
  start,tempInicial,tempMax,tempMed,tempMin,tempAlm,time1,time2,time3,time4,numCiclos
  
  Comandos adicionales:
  - pause: Pausa el proceso en el punto actual
  - cancel: Cancela y detiene completamente el programa
  
  Ejemplo:
  start,20.0,50.0,35.0,25.0,10.0,5,10,7,5,3
*/

#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Definir pines
#define ONE_WIRE_BUS 2 // Pin donde está conectado el sensor DS18B20
#define H_BRIDGE_UP 3   // Pin de control para aumentar la temperatura
#define H_BRIDGE_DOWN 4 // Pin de control para disminuir la temperatura

// Configurar sensor de temperatura
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Variables de control
float tempInicial, tempMax, tempMed, tempMin, tempAlm; // Temperaturas de referencia
int time1, time2, time3, time4; // Tiempos de espera entre temperaturas (en segundos)
int numCiclos;                  // Número de ciclos de control
String comando;
bool cicloActivo = false;        // Estado del ciclo de temperatura
bool cancelado = false;          // Estado de cancelación

void setup() { 
    Serial.begin(9600); // Iniciar comunicación serial
    sensors.begin();    // Iniciar el sensor de temperatura
    
    // Configurar pines del puente H como salidas
    pinMode(H_BRIDGE_UP, OUTPUT);
    pinMode(H_BRIDGE_DOWN, OUTPUT);
    
    // Inicializar pines en estado bajo (apagado)
    digitalWrite(H_BRIDGE_UP, LOW);
    digitalWrite(H_BRIDGE_DOWN, LOW);
}

void loop() {
    if (Serial.available() > 0) {
        comando = Serial.readStringUntil('\n');
        comando.trim();

        if (comando.startsWith("start")) {
            leerParametros(comando);
            cicloActivo = true;
            cancelado = false;
            Serial.println("Ciclo de temperatura iniciado");
        } else if (comando == "pause") {
            cicloActivo = false;
            Serial.println("Ciclo pausado");
        } else if (comando == "cancel") {
            cicloActivo = false;
            cancelado = true;
            Serial.println("Proceso cancelado");
        }
    }

    // Ejecutar ciclo de temperatura si está activo y no cancelado
    if (cicloActivo && !cancelado) {
        for (int i = 0; i < numCiclos; i++) {
            if (!cicloActivo || cancelado) break; // Detener en la iteración si se recibe "pause" o "cancel"
            Serial.print("Ciclo "); Serial.println(i + 1);
            
            // Llevar a temperatura inicial
            controlarTemperatura(tempInicial, time1);
            
            // Subir a temperatura máxima
            controlarTemperatura(tempMax, time2);
            
            // Bajar a temperatura media
            controlarTemperatura(tempMed, time3);
            
            // Bajar a temperatura mínima
            controlarTemperatura(tempMin, time4);
        }
        
        // Bajar la temperatura a tempAlm al final de los ciclos si no ha sido cancelado
        if (cicloActivo && !cancelado) {
            Serial.println("Bajando la temperatura de almacenamiento");
            controlarTemperatura(tempAlm, time4);
            Serial.println("Proceso finalizado");
            cicloActivo = false;
        }
    }
}

// Función para leer parámetros del puerto serial
void leerParametros(String datos) {
    datos.remove(0, 6); // Eliminar "start," del string
    
    int index = 0;
    tempInicial = extraerValor(datos, index);
    tempMax = extraerValor(datos, index);
    tempMed = extraerValor(datos, index);
    tempMin = extraerValor(datos, index);
    tempAlm = extraerValor(datos, index);
    time1 = extraerValor(datos, index);
    time2 = extraerValor(datos, index);
    time3 = extraerValor(datos, index);
    time4 = extraerValor(datos, index);
    numCiclos = extraerValor(datos, index);
    
    Serial.println("Datos recibidos correctamente");
}

// Función para extraer valores del string recibido
float extraerValor(String &datos, int &index) {
    int nextComma = datos.indexOf(',', index);
    float valor = datos.substring(index, nextComma).toFloat();
    index = nextComma + 1;
    return valor;
}

// Función para controlar la temperatura hacia un objetivo
void controlarTemperatura(float objetivo, int tiempoEspera) {
    Serial.print("Ajustando temperatura a "); Serial.println(objetivo);
    
    while (cicloActivo && !cancelado && abs(leerTemperatura() - objetivo) > 0.5) {
        if (leerTemperatura() < objetivo) {
            digitalWrite(H_BRIDGE_UP, HIGH);
            digitalWrite(H_BRIDGE_DOWN, LOW);
        } else {
            digitalWrite(H_BRIDGE_UP, LOW);
            digitalWrite(H_BRIDGE_DOWN, HIGH);
        }
        delay(tiempoEspera * 1000);
    }
    detenerControl();
}

// Función para leer la temperatura actual del sensor
float leerTemperatura() {
    sensors.requestTemperatures();
    float temp = sensors.getTempCByIndex(0);
    Serial.print("Temperatura actual: ");
    Serial.println(temp);
    return temp;
}

// Función para detener el control de temperatura
void detenerControl() {
    digitalWrite(H_BRIDGE_UP, LOW);
    digitalWrite(H_BRIDGE_DOWN, LOW);
    Serial.println("Control detenido");
}
