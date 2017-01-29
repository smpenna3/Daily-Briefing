#include "Adafruit_Thermal.h"
#include "SoftwareSerial.h"

#define TX_PIN 6 
#define RX_PIN 5

SoftwareSerial mySerial(RX_PIN, TX_PIN);
Adafruit_Thermal printer(&mySerial);

String wordReceived = "";
boolean stringComplete = false;


void setup() {
  Serial.begin(9600);
  mySerial.begin(19200);
  printer.begin();
}

void printtext(String words){
  printer.inverseOff();
  printer.println((words));
  printer.feed(1);
}


void loop() {
  while(Serial.available() > 0){
    char incomingByte = Serial.read();
    
    wordReceived += incomingByte;

    if(incomingByte == '|'){
      Serial.print("Printing: ");
      Serial.println(wordReceived.substring(0, wordReceived.length()-1));
      Serial.print("length: ");
      Serial.println(wordReceived.length()-1);

      printtext(wordReceived.substring(0, wordReceived.length()-1));
      wordReceived = "";
    } 
  }
}


