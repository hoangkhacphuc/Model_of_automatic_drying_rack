#include <wiringPi.h>

#define INP1 4
#define INP2 5
#define ENA 6

int main(void){
	wiringPiSetup();
	pinMode(INP1, OUTPUT);
    pinMode(INP2, OUTPUT);
    pinMode(ENA, OUTPUT);
    digitalWrite(INP1,LOW);
    digitalWrite(INP2,LOW);
    digitalWrite(ENA,LOW);
    // int direction = 0;

	for(;;){
        digitalWrite(INP1,LOW);
        digitalWrite(INP2,HIGH);
        digitalWrite(ENA,HIGH);

        // Giảm tốc độ 1 nửa (50%) sau 5 giây bằng pwm
        delay(5000);
        // change duty cycle trong c++
        pwmWrite(ENA, 50);
        delay(5000);
	}
	return 0;
}