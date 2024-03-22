int ledPin = 2;
int buttonPin1 = 10;
int buttonPin2 = 8;
int buttonPin3 = 12;
int buttonPin4 = 6;

bool button1State = false;
bool button2State = false;
bool button3State = false;
bool button4State = false;

void setup() {
    pinMode(ledPin, OUTPUT);
    pinMode(buttonPin1, INPUT_PULLUP);
    pinMode(buttonPin2, INPUT_PULLUP);
    pinMode(buttonPin3, INPUT_PULLUP);
    pinMode(buttonPin4, INPUT_PULLUP);
    Serial.begin(9600);
}

void loop() {
    
    if (digitalRead(buttonPin1) == LOW && !button1State) {
        digitalWrite(ledPin, HIGH);
        Serial.print("play:01/");
        button1State = true;
    } else if (digitalRead(buttonPin1) == HIGH) {
        button1State = false;
        digitalWrite(ledPin, LOW);
    }

    if (digitalRead(buttonPin2) == LOW && !button2State) {
        digitalWrite(ledPin, HIGH);
        Serial.print("play:02/");
        button2State = true;
    } else if (digitalRead(buttonPin2) == HIGH) {
        button2State = false;
        digitalWrite(ledPin, LOW);
    }

    // 나머지 버튼에 대한 코드도 추가할 수 있습니다.
}