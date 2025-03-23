#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2
#define H_BRIDGE_UP 3
#define H_BRIDGE_DOWN 4

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

float tempInicial, tempMax, tempMed, tempMin, tempAlm;
int time1, time2, time3, time4, numCiclos;
String comando;
bool cicloActivo = false;
bool cancelado = false;

void setup() {
    Serial.begin(9600);
    sensors.begin();
    pinMode(H_BRIDGE_UP, OUTPUT);
    pinMode(H_BRIDGE_DOWN, OUTPUT);
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
            Serial.println("Ciclo iniciado");
        } else if (comando == "pause") {
            cicloActivo = false;
            Serial.println("Ciclo pausado");
        } else if (comando == "cancel") {
            cicloActivo = false;
            cancelado = true;
            Serial.println("Proceso cancelado");
        }
    }

    if (cicloActivo && !cancelado) {
        for (int i = 0; i < numCiclos; i++) {
            if (!cicloActivo || cancelado) break;
            controlarTemperatura(tempInicial, time1);
            controlarTemperatura(tempMax, time2);
            controlarTemperatura(tempMed, time3);
            controlarTemperatura(tempMin, time4);
        }
        if (cicloActivo && !cancelado) {
            controlarTemperatura(tempAlm, time4);
            Serial.println("Proceso finalizado");
            cicloActivo = false;
        }
    }
}

void leerParametros(String datos) {
    datos.remove(0, 6);
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

float extraerValor(String &datos, int &index) {
    int nextComma = datos.indexOf(',', index);
    float valor = datos.substring(index, nextComma).toFloat();
    index = nextComma + 1;
    return valor;
}

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

float leerTemperatura() {
    sensors.requestTemperatures();
    float temp = sensors.getTempCByIndex(0);
    Serial.print("Temperatura actual: "); Serial.println(temp);
    return temp;
}

void detenerControl() {
    digitalWrite(H_BRIDGE_UP, LOW);
    digitalWrite(H_BRIDGE_DOWN, LOW);
    Serial.println("Control detenido");
}
