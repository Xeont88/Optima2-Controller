#include <AccelStepper.h>
AccelStepper stepper(1, 35, 37); // 1

#include "Parser.h"

void setup()
{
  stepper.setMaxSpeed(1500);
  stepper.setAcceleration(1000);

  Serial.begin(115200);
}

bool running = false;
void loop() {
  if (Serial.available()) {
    char buf[50];
    Serial.readBytesUntil(';', buf, 50);
    Parser data(buf, ',');
    int ints[10];
    data.parseInts(ints);
    switch (ints[0]) {
      // управление LED
      case 1:
        stepper.moveTo(ints[1]);
        running = true;
        break;
    }
  }
  if (stepper.distanceToGo() == 0 && running) {
    Serial.println("Ok");
    running = false;
  }
  stepper.run();
}
