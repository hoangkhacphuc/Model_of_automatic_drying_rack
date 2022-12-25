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

    // chỉnh tốc độ
    pwmSetRange(1024);
    pwmWrite(ENA, 100);

    int direction = 0;

	for(;;){
        // chạy liên tục
        if (direction == 0) {
            digitalWrite(INP1,LOW);
            digitalWrite(INP2,HIGH);
            digitalWrite(ENA,HIGH);
        }
        else {
            digitalWrite(INP1,HIGH);
            digitalWrite(INP2,LOW);
            digitalWrite(ENA,HIGH);
        }
	}
	return 0;
}