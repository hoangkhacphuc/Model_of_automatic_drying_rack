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
    pwmSetMode(PWM_MODE_MS);
    pwmSetRange(1024);

    // int direction = 0;

	for(;;){
        pwmWrite(ENA, 1024);
        digitalWrite(INP1,LOW);
        digitalWrite(INP2,HIGH);
        digitalWrite(ENA,HIGH);

        // Giảm tốc độ 1 nửa (50%) sau 5 giây bằng pwm
        delay(5000);
        pwmWrite(ENA, 1024/2);
        delay(5000);
	}
	return 0;
}