/*
   Данный код плавно управляет одной сервой (на пине 2)
   при помощи потенциометра (на пине А0).
   Откройте порт по последовательному соединению для наблюдения за положением серво
   Документация: https://alexgyver.ru/servosmooth/
*/

#include <ServoSmooth.h>
ServoSmooth servo;

uint32_t myTimer;

void setup() {
  Serial.begin(9600);
  servo.attach(A1, 600, 2400);  // 600 и 2400 - длины импульсов, при которых
  // серво поворачивается максимально в одну и другую сторону, зависят от самой серво
  // и обычно даже указываются продавцом. Мы их тут указываем для того, чтобы
  // метод setTargetDeg() корректно отрабатывал диапазон поворота сервы

  servo.setSpeed(90);   // ограничить скорость
  servo.setAccel(0.2);  	// установить ускорение (разгон и торможение)
}

void loop() {
  // желаемая позиция задаётся методом setTarget (импульс) или setTargetDeg (угол), далее
  // при вызове tick() производится автоматическое движение сервы
  // с заданным ускорением и ограничением скорости
  boolean state = servo.tick();   // здесь происходит движение серво по встроенному таймеру!


  if (millis() - myTimer >= 40) {
    myTimer = millis();
    int newPos = map(analogRead(A2), 0, 1023, 500, 2400); // берём с потенцометра значение 500-2400 (импульс)
    servo.setTarget(newPos);               // и отправляем на серво
    Serial.println(String(newPos) + " " + String(servo.getCurrent())/* + " " + String(state)*/);
	// state показывает сотояние сервы (0 - движется, 1 - приехали и отключились)
  }
}
