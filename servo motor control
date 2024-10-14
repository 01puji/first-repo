#include <Servo.h>

Servo myServo;
String str = "";

void setup() {
  Serial.begin(9600);
  myServo.attach(9); 
  Serial.println("5자리 숫자 입력하세요: ");
}

void loop() {
  if (Serial.available() > 0) {
    str = Serial.readStringUntil('\n');
    str.trim();

    if (str.length() == 5) {
      String coffee = str.substring(1, 2); 
      String cola = str.substring(2, 5);   
      
      Serial.print("입력한 숫자 = ");
      Serial.println(str);
      
      if (coffee == "0") {
        Serial.println("[motor rotation = left]");
      } else if (coffee == "1") {
        Serial.println("[motor rotation = right]");
      }

      delay(2000);

      int degree_angle = cola.toInt();  

      if (degree_angle >= 0 && degree_angle <= 180) {
       myServo.write(degree_angle);
       delay(15 * abs(degree_angle));
       Serial.print("최종 각도: ");
       Serial.println(degree_angle);
      } else {
        Serial.println("각도 범위는 0에서 180도 사이여야 합니다."); 
      }
    }
  }
}
