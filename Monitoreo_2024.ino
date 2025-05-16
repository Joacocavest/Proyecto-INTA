#include <TinyLoRa.h>
#include <SPI.h>
#include "DHT.h"
#include <Wire.h>
#include "LowPower.h"
#include <Adafruit_GPS.h>
#include <LoRa.h>

//NODO 1
/*uint8_t NwkSkey[16] = { 0x1A, 0x50, 0x03, 0x3E, 0x0A, 0xD3, 0x08, 0x7E, 0x0B, 0xF9, 0x23, 0x1C, 0xF7, 0xC3, 0xB8, 0x25 };
uint8_t AppSkey[16] = { 0xE7, 0xFB, 0xA8, 0x3E, 0xCD, 0xD7, 0xCB, 0xB1, 0x54, 0x45, 0xB7, 0xA8, 0xB4, 0xB3, 0xAB, 0xB5 };
uint8_t DevAddr[4] = { 0x26, 0x0D, 0x0A, 0x4C };
const char* DevAddrnodo = "260D0A4C";*/
//NODO 3
uint8_t NwkSkey[16] = { 0x1A, 0x50, 0x03, 0x3E, 0x0A, 0xD3, 0x08, 0x7E, 0x0B, 0xF9, 0x23, 0x1C, 0xF7, 0xC3, 0xB8, 0x25 };
uint8_t AppSkey[16] = { 0xE7, 0xFB, 0xA8, 0x3E, 0xCD, 0xD7, 0xCB, 0xB1, 0x54, 0x45, 0xB7, 0xA8, 0xB4, 0xB3, 0xAB, 0xB5 };
uint8_t DevAddr[4] = { 0x00, 0x00, 0x00, 0x01 };
const char* DevAddrnodo = "00000001";

unsigned char datasend[100];
String loraData;
int columna;

#define DHTPIN 12
#define GPSECHO false
#define DHTTYPE DHT11
#define VBATPIN A7
#define GPSSerial Serial1

DHT dht(DHTPIN, DHTTYPE);
Adafruit_GPS GPS(&GPSSerial);

bool gpsSignal = false;
uint32_t timer = millis();
int estado = 3, contador = 0;

// Pinout for Adafruit Feather 32u4 LoRa
TinyLoRa lora = TinyLoRa(7, 8, 4);

void Init_LoRa();

void setup() {
    pinMode(11, OUTPUT);
    digitalWrite(11, HIGH);
  
    Serial.begin(9600);
    while (!Serial);

    GPS.begin(9600);
    GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
    GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
    GPS.sendCommand(PGCMD_ANTENNA);

    delay(1000);
  
    Init_LoRa();

    Serial.println("OK");
}

void loop() {
      char datasend[loraData.length() + 1];
      loraData.toCharArray(datasend, sizeof(datasend));    
  
    switch (estado) {
        case 2: // Dormido
            digitalWrite(11, LOW);
            digitalWrite(LED_BUILTIN, LOW);
            for (int i = 0; i < 5; i++) {
                LowPower.idle(SLEEP_8S, ADC_OFF, TIMER4_OFF, TIMER3_OFF, TIMER1_OFF, TIMER0_OFF, SPI_OFF, USART1_OFF, TWI_OFF, USB_ON);
            }
            estado = 3;
            break;

        case 3: // Energizar
            digitalWrite(LED_BUILTIN, HIGH);
            digitalWrite(11, HIGH);
            delay(10000);
            estado = 4;
            break;

        case 4: // Leer Sensores
            gpsSignal = leerGPS();
            if (gpsSignal) {
                estado = 5;
            } else {
                estado = 4; // seguir buscando señal
            }
            break;

        case 5: // LORA
            enviarDatosLoRa();
            estado = 2;
            break;
    }
}

void Init_LoRa() {
    Serial.print("Starting LoRa...");
    lora.setChannel(CH2);
    lora.setDatarate(SF7BW125);
    if (!lora.begin()) {
        Serial.println("Failed");
        Serial.println("Check your radio");
        while (true);
    }
   
    Serial.println("OK");
}

bool leerGPS() {
    char c = GPS.read();
    if (GPSECHO && c) Serial.print(c);

    if (GPS.newNMEAreceived()) {
        if (!GPS.parse(GPS.lastNMEA())) return false;
    }

    if (millis() - timer > 2000) {
        timer = millis();
        if (GPS.fix) {
            Serial.print("Location: ");
            Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
            Serial.print(", ");
            Serial.print(GPS.longitude, 4); Serial.println(GPS.lon);
            return true;
        }
    }
    return false;
}

void enviarDatosLoRa() {
  
    /*char loraData[100];
    snprintf(loraData, sizeof(loraData), "%s;%02d/%02d/20%02d;%02d:%02d:%02d;%f;%f;%d;", 
             DevAddrnodo, GPS.day, GPS.month, GPS.year, GPS.hour, GPS.minute, GPS.seconds, 
             GPS.latitude, GPS.longitude);

   Serial.println("Enviando Paquete LoRa ....");
 
   lora.sendData(loraData, sizeof(loraData), lora.frameCounter);
    delay (1000);*/
     Serial.println("////MOSTRANDO FECHA, HORA Y DATOS DE UBICACIÓN////");
   
                  loraData = "";                   
                  for (columna = 1; columna <= 7; columna++) {

                  if (columna == 1){
                     //loraData +=  String("260D0A4C"); 
                     //loraData +=  String("260D6CDE"); 
                     loraData+= String(DevAddrnodo);
                  }
                 if (columna == 2){
                    //FECHA de GPS
                      loraData += String(GPS.day);
                      loraData += "/";
                      loraData += String(GPS.month, DEC);
                      loraData += "/20";
                      loraData += String(GPS.year, DEC);
                    //Envio dato fijo FECHA
                   
                       }
                     if (columna == 3){
                        //HORA de GPS
                           loraData += String(GPS.hour);
                           loraData += ":"; 
                           loraData += String(GPS.minute);
                           loraData += ":"; 
                           loraData += String(GPS.seconds, DEC);
                                                     
                        //Envio dato fijo HORA
                        
                        } 
                           
                      if (columna == 4){
                          //LATITUD de GPS
                          //latitud = (GPS.latitude);
                           //loraData += String(latitud);
                           loraData += String(GPS.latitude, 4);
                           //loraData +='.';
                           //lat_dec= (GPS.lat, DEC);
                           loraData += (GPS.lat); 
                        //Envio dato fijo LATITUD
                                                        
                        }
                        
                       if (columna == 5) {
                          //LONGITUD de GPS
                         // longitud = (GPS.longitude);                                
                          loraData += String(GPS.longitude, 4);
                          loraData += (GPS.lon);
                          //Envio dato fijo LONGITUD
                        
                       }                                    
                                                                         
                     if (columna == 6) {
                           loraData += String(contador);
                       }
                        
                       if (columna < 7) {
                          loraData += ";";
                       }
                       }
                      contador++;
                   
                      Serial.println(loraData);
                      Serial.println("Enviando Paquete LoRa ....");
                

                      lora.sendData(datasend, sizeof(datasend),lora.frameCounter);
                  
  
                       Serial.println("Espere......");
}
