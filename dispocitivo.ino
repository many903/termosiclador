#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Definir pines
#define ONE_WIRE_BUS 2 // Pin donde está conectado el sensor de temperatura DS18B20
#define H_BRIDGE_UP 3   // Pin de control para aumentar la temperatura
#define H_BRIDGE_DOWN 4 // Pin de control para disminuir la temperatura

// Configurar sensor de temperatura
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Variables de control
float tempMax, tempMin, tempMed; // Temperaturas de referencia
int numCiclos;                   // Número de ciclos de control
unsigned long tiempo;             // Tiempo de espera entre mediciones
bool cicloActivo = false;         // Estado del ciclo de temperatura

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
        String comando = Serial.readStringUntil('\n');
        comando.trim();

        if (comando == "play") {
            cicloActivo = true;
            Serial.println("Ciclo de temperatura iniciado");
        } else if (comando == "pause") {
            cicloActivo = false;
            Serial.println("Ciclo pausado");
        } else {
            // Leer datos del puerto serial en el orden esperado
            tempMax = comando.toFloat(); // Temperatura máxima permitida
            tempMin = Serial.parseFloat(); // Temperatura mínima permitida
            tempMed = Serial.parseFloat(); // Temperatura media de referencia
            numCiclos = Serial.parseInt(); // Número de ciclos a ejecutar
            tiempo = Serial.parseInt();    // Tiempo de espera entre mediciones (en segundos)
            Serial.println("Datos recibidos correctamente");
        }
    }

    // Ejecutar ciclo de temperatura si está activo
    if (cicloActivo) {
        for (int i = 0; i < numCiclos; i++) {
            if (!cicloActivo) break; // Detener en la iteración si se recibe "pause"
            Serial.print("Ciclo "); Serial.println(i + 1);
            
            // Subir a temperatura máxima
            while (leerTemperatura() < tempMax && cicloActivo) {
                digitalWrite(H_BRIDGE_UP, HIGH);
                digitalWrite(H_BRIDGE_DOWN, LOW);
                delay(tiempo * 1000);
            }
            detenerControl();
            
            // Bajar a temperatura media
            while (leerTemperatura() > tempMed && cicloActivo) {
                digitalWrite(H_BRIDGE_UP, LOW);
                digitalWrite(H_BRIDGE_DOWN, HIGH);
                delay(tiempo * 1000);
            }
            detenerControl();
            
            // Bajar a temperatura mínima
            while (leerTemperatura() > tempMin && cicloActivo) {
                digitalWrite(H_BRIDGE_UP, LOW);
                digitalWrite(H_BRIDGE_DOWN, HIGH);
                delay(tiempo * 1000);
            }
            detenerControl();
        }
        
        // Bajar la temperatura a -5°C al final del número de ciclos
        if (cicloActivo) {
            Serial.println("Bajando la temperatura a -5°C");
            while (leerTemperatura() > -5.0 && cicloActivo) {
                digitalWrite(H_BRIDGE_UP, LOW);
                digitalWrite(H_BRIDGE_DOWN, HIGH);
                delay(tiempo * 1000);
            }
            detenerControl();
            Serial.println("Proceso finalizado");
            cicloActivo = false;
        }
    }
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