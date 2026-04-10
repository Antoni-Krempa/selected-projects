#include <Servo.h>

//  Piny sterownika jak w nowym układzie
const int PUL_PLUS  = 4;
const int DIR_PLUS  = 8;
const int ENA_PLUS  = 10;

const int PUL_MINUS = 7;
const int DIR_MINUS = 9;
const int ENA_MINUS = 12;

// Przycisk awaryjny 
const int BTN_ESTOP = 2;      // STOP awaryjny na D2
bool emergencyStop = false;

// Serwo 
const int SERVO_PIN = 6;
Servo myServo;

// Parametry silnika 
const int STEPS_PER_REV = 200;      // pełne kroki silnika
const int MICROSTEPPING  = 8;

//  Rampa (docelowe długości, gdy ruch jest długi)
const long ACCEL_STEPS_BASE = 100L * MICROSTEPPING;
const long DECEL_STEPS_BASE = 100L * MICROSTEPPING;

// czasy bazowe 
const long BASE_MIN_DELAY = 3000;    // µs docelowa max prędkość
const long BASE_MAX_DELAY = 20000;   // µs start/stop

// przeskalowane pod mikrostep
const long MIN_DELAY = BASE_MIN_DELAY / MICROSTEPPING;
const long MAX_DELAY = BASE_MAX_DELAY / MICROSTEPPING;

//przykładowa lista instukcji
int positions[100] = {
  0, 112, 57, 183, 41, 196, 74, 129, 9, 166,
  88, 143, 37, 154, 22, 191, 63, 118, 5, 147,
  81, 173, 14, 102, 49, 187, 27, 160, 96, 135,
  18, 178, 68, 120, 3, 151, 84, 194, 32, 140,
  55, 170, 12, 108, 45, 182, 25, 132, 77, 159,
  6, 167, 90, 138, 52, 189, 28, 104, 63, 176,
  11, 153, 72, 124, 4, 148, 87, 193, 36, 115,
  58, 181, 23, 130, 71, 164, 8, 144, 95, 199,
  34, 121, 50, 174, 16, 157, 69, 136, 1, 149,
  83, 185, 39, 110, 47, 172, 19, 134, 62, 0
};

int listSize = sizeof(positions) / sizeof(positions[0]);

// Zmienne ruchu 
long TOTAL_STEPS = 0;
long stepCounter = 0;

long accelStepsEff = 0;   // ile kroków faktycznie na przyspieszanie
long decelStepsEff = 0;   // ile kroków faktycznie na hamowanie

bool directionCW = true;  // true = HIGH na DIR_MINUS


// Przyciski 

bool isPressed(int pin) {
  return (digitalRead(pin) == LOW);
}


// STOP awaryjny – wyłącza driver odłącza serwo  

void doEmergencyStop() {
  emergencyStop = true;

  // wyłącz driver
  digitalWrite(ENA_MINUS, LOW);
  digitalWrite(ENA_PLUS,  LOW);

  // odłącz serwo
  myServo.detach();

  //koniec programu
  while (true) {
   
  }
}


// Gładki ruch serwa z kąta fromAngle do toAngle

void moveServoSmooth(int fromAngle, int toAngle) {
  if (fromAngle == toAngle || emergencyStop) return;

  int step = (toAngle > fromAngle) ? 1 : -1;

  for (int a = fromAngle; a != toAngle + step && !emergencyStop; a += step) {
    if (isPressed(BTN_ESTOP)) {
      doEmergencyStop();
    }
    myServo.write(a);
    delay(25);  // prędkość serwa
  }
}


// Mała sekwencja: serwo - krokowiec - serwo

void runServoStepSequence() {
  if (emergencyStop) return;

  // serwo góra
  moveServoSmooth(10, 140);
  if (emergencyStop) return;

  // 40 impulsów w prawo 
  digitalWrite(DIR_MINUS, HIGH);

  for (int i = 0; i < 40 && !emergencyStop; i++) {
    if (isPressed(BTN_ESTOP)) {
      doEmergencyStop();
    }

    // krok
    digitalWrite(PUL_MINUS, LOW);
    delayMicroseconds(8000);
    digitalWrite(PUL_MINUS, HIGH);
    delayMicroseconds(8000);
  }

  if (emergencyStop) return;

  // serwo dół
  moveServoSmooth(140, 10);
}

// Przygotowanie ruchu głównego (rampa) 

void computeMove(int x1, int x2) {
  // Różnica po okręgu 200
  int d = (x1 - x2 + 200) % 200;

  if (d > 100) {
    d = 200 - d;        // krótsza droga
    directionCW = false;
  } else {
    directionCW = true;
  }

  //  REVS = d * 5
  float revs = d / 40.0f;

  //  Kroki całkowite
  TOTAL_STEPS = (long)(revs * STEPS_PER_REV * MICROSTEPPING);

  if (TOTAL_STEPS <= 0) {
    accelStepsEff = 0;
    decelStepsEff = 0;
    return;
  }

  //  Ustaw kierunek
  digitalWrite(DIR_MINUS, directionCW ? HIGH : LOW);

  //  Rampa: pełny trapez lub trójkąt
  long half = TOTAL_STEPS / 2;

  if (TOTAL_STEPS >= 2 * ACCEL_STEPS_BASE) {
    //  trapez
    accelStepsEff = ACCEL_STEPS_BASE;
    decelStepsEff = ACCEL_STEPS_BASE;
  } else {
    // trójkąt 
    accelStepsEff = half;
    decelStepsEff = TOTAL_STEPS - accelStepsEff;
  }

  stepCounter = 0;
}

// SETUP

void setup() {
  // plusy
  pinMode(PUL_PLUS, OUTPUT);
  pinMode(DIR_PLUS, OUTPUT);
  pinMode(ENA_PLUS, OUTPUT);
  digitalWrite(PUL_PLUS, HIGH);  // PUL+ = 5 V
  digitalWrite(DIR_PLUS, HIGH);  // DIR+ = 5 V
  digitalWrite(ENA_PLUS, HIGH);  // ENA+ = 5 V 

  // minusy
  pinMode(PUL_MINUS, OUTPUT);
  pinMode(DIR_MINUS, OUTPUT);
  pinMode(ENA_MINUS, OUTPUT);

  digitalWrite(DIR_MINUS, HIGH);
  digitalWrite(ENA_MINUS, HIGH);  // włączony driver 
  digitalWrite(PUL_MINUS, HIGH);

  // przycisk awaryjny
  pinMode(BTN_ESTOP, INPUT_PULLUP);

  // serwo
  myServo.attach(SERVO_PIN);
  myServo.write(10);

  delay(3000);
}


void loop() {
  // Przelatujemy listę parami
  for (int i = 0; i < listSize - 1 && !emergencyStop; i++) {
    int x1 = positions[i];
    int x2 = positions[i + 1];

    computeMove(x1, x2);
    if (TOTAL_STEPS <= 0) {
      continue;
    }

    long constStart = accelStepsEff;
    long constEnd   = TOTAL_STEPS - decelStepsEff;

    while (stepCounter < TOTAL_STEPS && !emergencyStop) {
      // EMERGENCY CHECK 
      if (isPressed(BTN_ESTOP)) {
        doEmergencyStop();
      }

      long pulseDelay;

      if (stepCounter < accelStepsEff) {
        // PRZYSPIESZANIE
        long idx = stepCounter;
        if (idx > ACCEL_STEPS_BASE) idx = ACCEL_STEPS_BASE;
        pulseDelay = map(idx, 0, ACCEL_STEPS_BASE, MAX_DELAY, MIN_DELAY);
      }
      else if (stepCounter >= constStart && stepCounter < constEnd) {
        // STAŁA PRĘDKOŚĆ 
        long idx = accelStepsEff;
        if (idx > ACCEL_STEPS_BASE) idx = ACCEL_STEPS_BASE;
        pulseDelay = map(idx, 0, ACCEL_STEPS_BASE, MAX_DELAY, MIN_DELAY);
      }
      else {
        // HAMOWANIE
        long idxFromEnd = TOTAL_STEPS - 1 - stepCounter;
        if (idxFromEnd > ACCEL_STEPS_BASE) idxFromEnd = ACCEL_STEPS_BASE;
        pulseDelay = map(idxFromEnd, 0, ACCEL_STEPS_BASE, MAX_DELAY, MIN_DELAY);
      }

      if (pulseDelay < MIN_DELAY) pulseDelay = MIN_DELAY;
      if (pulseDelay > MAX_DELAY) pulseDelay = MAX_DELAY;

      digitalWrite(PUL_MINUS, LOW);
      delayMicroseconds(pulseDelay);
      digitalWrite(PUL_MINUS, HIGH);
      delayMicroseconds(pulseDelay);

      stepCounter++;
    }

    if (emergencyStop) {
      break;
    }

    // sekwencja serwo-krokowiec-serwo
    runServoStepSequence();

    if (emergencyStop) {
      break;
    }

    delay(1000);  // pauza między punktami
  }

  // po przejściu całej tablicy – stop na zawsze
  while (true) { }
}
