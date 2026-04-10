#include <Servo.h>

// SERWO 
Servo myServo;
int aktualnyKat = 180;  

// Piny sterownika krokowca 
const int PUL_PLUS  = 4;
const int DIR_PLUS  = 8;
const int ENA_PLUS  = 10;

const int PUL_MINUS = 7;
const int DIR_MINUS = 9;
const int ENA_MINUS = 12;

// BTS7960 
const int L_EN  = 5;
const int R_EN  = 6;
const int L_PWM = 3;    // PWM (Timer2)
const int R_PWM = 11;   // PWM (Timer2)

// Parametry kroku 
const int LOGIC_STEP_PULSES = 40;        // 1 krok = 40 impulsów (przekładnia + mikrokroki)
const int STEP_DELAY_US     = 10000;     // 10 ms między zboczami  

// Awaryjny stop 
const int EMERGENCY_PIN = 13;
bool emergencyStop = false;

// FUNKCJA AWARYJNEGO STOPU
void handleEmergency() {
  if (emergencyStop) return;  // już wyłączone

  emergencyStop = true;

  // Wyłącz silnik DC
  analogWrite(R_PWM, 0);
  analogWrite(L_PWM, 0);
  digitalWrite(L_EN, LOW);
  digitalWrite(R_EN, LOW);

  // Wyłącz sterownik krokowy (cewki puszczone)
  digitalWrite(ENA_MINUS, LOW);   // zakładamy, że LOW = disable
  digitalWrite(ENA_PLUS, LOW);

  // Wyłącz serwo
  myServo.detach();
}

void setup() {
  // SERWO 
  myServo.attach(2);           // serwo na pinie 2
  myServo.write(aktualnyKat);  // łagodny start w pozycję 180 stioni
  delay(500);

  // BTS7960
  pinMode(L_EN, OUTPUT);
  pinMode(R_EN, OUTPUT);
  pinMode(L_PWM, OUTPUT);
  pinMode(R_PWM, OUTPUT);

  digitalWrite(L_EN, HIGH);   // włącz driver po stronie L
  digitalWrite(R_EN, HIGH);   // włącz driver po stronie R

  // Ustawienie szybkiego PWM na Timer2
  // Timer2: Fast PWM, preskaler 8  ~7,8 kHz na pinach 3 i 11
  TCCR2B = (TCCR2B & 0b11111000) | 0x02;  // preskaler = 8

  // stałe obroty silnika DC
  analogWrite(R_PWM, 140);  
  analogWrite(L_PWM, 0);    

  // KROKOWIEC
  // plusy jako stałe +5 V
  pinMode(PUL_PLUS, OUTPUT);
  pinMode(DIR_PLUS, OUTPUT);
  pinMode(ENA_PLUS, OUTPUT);
  digitalWrite(PUL_PLUS, HIGH);
  digitalWrite(DIR_PLUS, HIGH);
  digitalWrite(ENA_PLUS, HIGH);

  // minusy sterujące z Arduino
  pinMode(PUL_MINUS, OUTPUT);
  pinMode(DIR_MINUS, OUTPUT);
  pinMode(ENA_MINUS, OUTPUT);

  // Kierunek
  digitalWrite(DIR_MINUS, HIGH);

  // Silnik krokowy włączony 
  digitalWrite(ENA_MINUS, HIGH);
  digitalWrite(PUL_MINUS, HIGH);

  //  Przycisk awaryjny
  pinMode(EMERGENCY_PIN, INPUT_PULLUP);   // przycisk do GND
}

// 1 krok = 40 impulsów PUL
void wykonajJedenKrokLogiczny() {
  for (int i = 0; i < LOGIC_STEP_PULSES; i++) {
    // sprawdź STOP w trakcie ruchu
    if (!emergencyStop && digitalRead(EMERGENCY_PIN) == LOW) {
      handleEmergency();
      return;
    }

    digitalWrite(PUL_MINUS, LOW);
    delayMicroseconds(STEP_DELAY_US);
    digitalWrite(PUL_MINUS, HIGH);
    delayMicroseconds(STEP_DELAY_US);
  }

}

void wykonajRuchSerwemDolGora() {
  // 180 -> 80
  for (int kat = aktualnyKat; kat >= 79; kat--) {
    if (emergencyStop) return;  
    if (digitalRead(EMERGENCY_PIN) == LOW && !emergencyStop) {
      handleEmergency();
      return;
    }

    myServo.write(kat);
    delay(25);
  }
  aktualnyKat = 79;


  for (int kat = aktualnyKat; kat <= 180; kat++) {
    if (emergencyStop) return;
    if (digitalRead(EMERGENCY_PIN) == LOW && !emergencyStop) {
      handleEmergency();
      return;
    }

    myServo.write(kat);
    delay(25);
  }
  aktualnyKat = 180;
}

void loop() {

  if (!emergencyStop && digitalRead(EMERGENCY_PIN) == LOW) {
    handleEmergency();
  }

  if (emergencyStop) {
 
    return;
  }



  // sekwencja serwa
  wykonajRuchSerwemDolGora();
  if (emergencyStop) return;

  // sekwencja ramy
  wykonajJedenKrokLogiczny();
  if (emergencyStop) return;
}
