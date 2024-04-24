#include <stdio.h>
#include <stdlib.h>
#include <string.h>
const int buttonPin1 = 2;
const int buttonPin2 = 3;
const int buttonPin3 = 4;
const int buttonPin4 = 5;

const int sliderPin1 = A0;
const int sliderPin2 = A1;
const int sliderPin3 = A2;
const int sliderPin4 = A3;
const int joyStickPinx = A14;
const int joyStickPiny = A15;
bool button1State = false;
bool button2State = false;
bool button3State = false;
bool button4State = false;

int val;
void setup() {
    pinMode(buttonPin1, INPUT_PULLUP);
    pinMode(buttonPin2, INPUT_PULLUP);
    pinMode(buttonPin3, INPUT_PULLUP);
    pinMode(buttonPin4, INPUT_PULLUP);
    pinMode(sliderPin1, INPUT);
    pinMode(sliderPin2, INPUT);
    pinMode(sliderPin3, INPUT);
    pinMode(sliderPin4, INPUT);
    Serial.begin(9600);
}

void loop() {
    if (digitalRead(buttonPin1) == LOW && !button1State) {
        Serial.println("digitalRead/incr:01");
        button1State = true;
    } else if (digitalRead(buttonPin1) == HIGH) {
        button1State = false;
    }

    if (digitalRead(buttonPin2) == LOW && !button2State) {
        Serial.println("digitalRead/incr:02");
        button2State = true;
    } else if (digitalRead(buttonPin2) == HIGH) {
        button2State = false;
    }

    if (digitalRead(buttonPin3) == LOW && !button3State) {
        Serial.println("digitalRead/incr:03");
        button3State = true;
    } else if (digitalRead(buttonPin3) == HIGH) {
        button3State = false;
    }

    if (digitalRead(buttonPin4) == LOW && !button4State) {
        Serial.println("digitalRead/incr:04");
        button4State = true;
    } else if (digitalRead(buttonPin4) == HIGH) {
        button4State = false;
    }

    int sliderValue1 = analogRead(sliderPin1);
    int sliderValue2 = analogRead(sliderPin2);
    int sliderValue3 = analogRead(sliderPin3);
    int sliderValue4 = 1023; 
    int joyStickValue1 = analogRead(joyStickPinx);
    int joyStickValue2 = analogRead(joyStickPiny);

    String sliderOutputString = "analogRead/slider1: " + String(sliderValue1) + ", slider2: " + String(sliderValue2) + ", slider3: " + String(sliderValue3) + ", slider4: " + String(sliderValue4);
    Serial.println(sliderOutputString);
    String joyStickOutputString = "analogRead/joyX: " + String(joyStickValue1) + ", joyY: " + String(joyStickValue2);
    //Serial.println(joyStickOutputString);
    delay(10);

    static unsigned long prevMillis = 0;
    const unsigned long interval = 100; // Adjust interval as needed
    
    /*if (millis() - prevMillis >= interval) {
      prevMillis = millis();
      float speed = 0.5*sin(prevMillis * 0.005) + 1 ; // Generate sine wave between -1 and 1, and map it to speed range
      Serial.print("analogRead/tape:");
      Serial.println(speed, 3); // Send speed value with 3 decimal places
    }*/

}
