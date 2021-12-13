#include <AccelStepper.h>
#include "Parser.h"
#include <FastLED.h>
#include <SoftwareSerial.h>
#include <DFPlayer_Mini_Mp3.h>
#include <ServoSmooth.h>

SoftwareSerial mySerial(3, 4); // RX, TX

#define NUM_LEDS 4+8+20
#define DATA_PIN 12
CRGB leds[NUM_LEDS];



#define PUMP_PIN   8
#define LASER_PIN 10

AccelStepper stepper1(1, 35, 37); // 1
AccelStepper stepper2(1, 46, 48); // 2, 3
AccelStepper stepper3(1, 23, 25); // 4
AccelStepper stepper4(1, 26, 28); // 5
AccelStepper stepper5(1, 34, 36); // 6
AccelStepper stepper7(1, 40, 42); //  карусель

#define SERVO_AXIS_6  9
ServoSmooth servo_axis_6;
#define SERVO_GRIPPER  11
ServoSmooth servo_gripper;

void setup() {
  //  stepper4.runSpeed();
  //  stepper5.runSpeed();

  FastLED.addLeds<WS2812, DATA_PIN, BRG>(leds, NUM_LEDS);

  Serial.flush();
  stepper1.setMaxSpeed(1500);
  stepper2.setMaxSpeed(600);
  stepper3.setMaxSpeed(2000);
  stepper4.setMaxSpeed(4000);
  stepper5.setMaxSpeed(800);
  stepper7.setMaxSpeed(1000);

  servo_axis_6.attach(SERVO_AXIS_6, 600, 2400);  // 600 и 2400 - длины импульсов, при которых
  servo_axis_6.setSpeed(180);   // ограничить скорость
  servo_axis_6.setAccel(0.8);   // установить ускорение (разгон и торможение)
  servo_axis_6.setTargetDeg(90);
  
  servo_gripper.attach(SERVO_GRIPPER, 600, 2400);  // 600 и 2400 - длины импульсов, при которых
  servo_gripper.setSpeed(180);   // ограничить скорость
  servo_gripper.setAccel(0.8);   // установить ускорение (разгон и торможение)
  //  servo_gripper.setAutoDetach(false); // отключить автоотключение (detach) при достижении целевого угла (по умолчанию включено)

  stepper1.setAcceleration(2000);
  stepper2.setAcceleration(2000);
  stepper3.setAcceleration(2000);
  stepper4.setAcceleration(2000);
  stepper5.setAcceleration(2000);
  stepper7.setAcceleration(2000);


  stepper1.setCurrentPosition(0 * 88);
  stepper2.setCurrentPosition(0 * 45);
  stepper3.setCurrentPosition(0 * 98);
  stepper4.setCurrentPosition(0 * 46);
  stepper5.setCurrentPosition(0 * 20);
  stepper7.setCurrentPosition(0 * 8.9);

  Serial.begin(115200);
  while (!Serial);
  
  pinMode(LASER_PIN, 1);
  pinMode(PUMP_PIN, 1);
  

  // DF-Player settings
  mySerial.begin (9600);
  mp3_set_serial (mySerial);  //set softwareSerial for DFPlayer-mini mp3 module
  delay (100);
  mp3_set_volume (10);

}



bool running = false;

void loop() {

  if (Serial.available()) {
    char buf[50];
    Serial.readBytesUntil(';', buf, 50);    // 1, 0, 90, 0, 0, 0, 0, 0;
    Parser data(buf, ',');
    int ints[10];
    data.parseInts(ints);

    switch (ints[0]) {
      // ****************** управление LASER ******************
      case 0:
        digitalWrite(LASER_PIN, ints[1]);
        //        Serial.print(ints[1]);
        if (ints[1]) {
          mp3_stop();
          delay (100);
          mp3_play_physical(2);
        } else {
          mp3_stop();
        }
        break;

      // ****************** управление двигателями ******************
      case 1:
        if (stepper1.currentPosition() != ints[1])
          stepper1.moveTo(ints[1] * 88);
        if (stepper2.currentPosition() != ints[2])
          stepper2.moveTo(ints[2] * 45);
        if (stepper3.currentPosition() != -ints[3])   //  ******************вернуть********************
          stepper3.moveTo(-ints[3] * 98);
        if (stepper4.currentPosition() != ints[4])
          stepper4.moveTo(ints[4] * 46);
        if (stepper5.currentPosition() != ints[5])
          stepper5.moveTo(ints[5] * 20);
          
        servo_axis_6.setTargetDeg(ints[6]+120);
        
        servo_gripper.setTargetDeg(ints[7]+80);
        if (stepper7.currentPosition() != ints[8])
          stepper7.moveTo(ints[8] * 8.9);       //  8.9 - коэфициент - "шаги в градусы"

        if (ints[9] != 9)   // если движение "домой", не менять состояние воздушной помпы
        digitalWrite(PUMP_PIN, ints[9]);
        
        running = true;   // робот начал движение
        break;

      // ****************** управление адресной LED лентой ******************
      case 2:
        for (int i = 0; i < NUM_LEDS; i++) {
          leds[i] = CRGB(ints[1], ints[2], ints[3]);
        }
        FastLED.show();
        break;

      // ****************** управление DF-player ******************
      case 5:     // 5, 3;
        Serial.print(ints[1]);
        if (ints[1] == 0)
          mp3_stop();
        else {
          mp3_stop();
          delay (100);
          mp3_play_physical(ints[1]);
          if (ints[1] == 4) {
            rom_dom_dom();
          }
        }
        break;
    }
  }

  stepper1.run();
  stepper2.run();
  stepper3.run();
  stepper4.run();
  stepper5.run();
  bool is_gripper_run = servo_gripper.tick();   // здесь происходит движение серво по встроенному таймеру!
  servo_axis_6.tick();
  stepper7.run();

  // Если все приводы завершили движение
  if (stepper1.distanceToGo() == 0 &&
      stepper2.distanceToGo() == 0 &&
      stepper3.distanceToGo() == 0 &&
      stepper4.distanceToGo() == 0 &&
      stepper5.distanceToGo() == 0 &&
      is_gripper_run               &&
      stepper7.distanceToGo() == 0 && running) {
    Serial.println("O");
    running = false;
  }


}


void rom_dom_dom() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB(255, 0, 0);
  }
  FastLED.show();
  delay(1000);
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB(0, 255, 0);
  }
  FastLED.show();
  delay(1000);
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB(0, 0, 255);
  }
  FastLED.show();
  delay(1000);
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB(0, 0, 0);
  }
  FastLED.show();
  delay(1000);
}
