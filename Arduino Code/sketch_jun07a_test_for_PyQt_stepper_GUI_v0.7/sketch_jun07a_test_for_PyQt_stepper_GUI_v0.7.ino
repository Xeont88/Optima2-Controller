#include <AccelStepper.h>
#include "Parser.h"
#include <FastLED.h>
#include <SoftwareSerial.h>
#include <DFPlayer_Mini_Mp3.h>
#include <ServoSmooth.h>

SoftwareSerial mySerial(3, 4); // RX, TX

//#define NUM_LEDS 4+8+20
#define NUM_LEDS (4+8)*3
#define DATA_PIN 12
CRGB leds[NUM_LEDS];



#define LED_PIN 10

AccelStepper stepper1(1, 35, 37); // 1
AccelStepper stepper2(1, 46, 48); // 2, 3
AccelStepper stepper3(1, 23, 25); // 4
AccelStepper stepper4(1, 26, 28); // 5
AccelStepper stepper5(1, 34, 36); // 6
AccelStepper stepper7(1, 40, 42); //  карусель

#define SERVO_AXIS_7  9
ServoSmooth servo_axis_7;
#define SERVO_GRIPPER  11
ServoSmooth servo_gripper;

void setup() {
  //  stepper4.runSpeed();
  //  stepper5.runSpeed();

//  FastLED.addLeds<WS2812, DATA_PIN, BRG>(leds, NUM_LEDS);
  FastLED.addLeds<WS2812, DATA_PIN, RGB>(leds, NUM_LEDS);

  Serial.flush();
  stepper1.setMaxSpeed(1500);
  stepper2.setMaxSpeed(600);
  stepper3.setMaxSpeed(2000);
  stepper4.setMaxSpeed(4000);
  stepper5.setMaxSpeed(800);
  stepper7.setMaxSpeed(1000);

  servo_axis_7.attach(SERVO_AXIS_7, 600, 2400);  // 600 и 2400 - длины импульсов, при которых
  servo_axis_7.setSpeed(180);   // ограничить скорость
  servo_axis_7.setAccel(0.8);   // установить ускорение (разгон и торможение)
  servo_axis_7.setTargetDeg(90);
  
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
  stepper4.setCurrentPosition(0 * 9);   // 46
  stepper5.setCurrentPosition(0 * 20);
  stepper7.setCurrentPosition(0 * 8.9);

  Serial.begin(115200);
  while (!Serial);
  pinMode(LED_PIN, 1);

  // DF-Player settings
//  mySerial.begin (9600);
  mp3_set_serial (mySerial);  //set softwareSerial for DFPlayer-mini mp3 module
  mp3_set_volume (15);

}

void loop() {

  if (Serial.available()) {
    char buf[50];
    Serial.readBytesUntil(';', buf, 50);
    Parser data(buf, ',');
    int ints[10];
    data.parseInts(ints);

    switch (ints[0]) {
      // управление LED
      case 0:
        digitalWrite(LED_PIN, ints[1]);
        break;

      // управление двигателями
      case 1:
        //        int position1 = ints[1];
        //        int position2 = ints[2];
        //        int position3 = ints[3];
        //        int position4 = ints[4];
        //        int position5 = ints[5];
        //        int position7 = ints[7];
        if (stepper1.currentPosition() != ints[1])
          stepper1.moveTo(ints[1] * 88);          // 88
        if (stepper2.currentPosition() != ints[2])
          stepper2.moveTo(ints[2] * 45);          // 45
        if (stepper3.currentPosition() != ints[3])
          stepper3.moveTo(ints[3] * 98);          // 98
        if (stepper4.currentPosition() != ints[4])
          stepper4.moveTo(ints[4] * 9);           // 46
        if (stepper5.currentPosition() != ints[5])
          stepper5.moveTo(ints[5] * 20);          // 20

//        if ();
        servo_axis_7.setTargetDeg(ints[6]+90);               
        
        servo_gripper.setTargetDeg(ints[7]);               

        if (stepper7.currentPosition() != ints[8])
          stepper7.moveTo(ints[8] * 8.9);       //  8.9 - коэфициент - "шаги в градусы"
        break;
        
      // управление адресной LED лентой
      case 2:
        for (int i = 0; i < NUM_LEDS; i++) {
          leds[i] = CRGB(ints[1], ints[2], ints[3]);

        }
        FastLED.show();
        break;

      case 5:
        if (ints[1] == 9)
          mp3_stop();
        else
          mp3_play(ints[1]);

        break;
    }
  }

  //  stepper4.runSpeedToPosition();
  //  stepper5.runSpeedToPosition();
  stepper1.run();
  stepper2.run();
  stepper3.run();
  stepper4.run();
  stepper5.run();
  servo_axis_7.tick();
  servo_gripper.tick();   // здесь происходит движение серво по встроенному таймеру!
  stepper7.run();
}
