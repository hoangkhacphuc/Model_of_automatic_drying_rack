#include <wiringPi.h>

#define INP1 0
#define INP2 2
#define ENA 1

int main(void){
	wiringPiSetup();
	pinMode(INP1, OUTPUT);
    pinMode(INP2, OUTPUT);
    pinMode(ENA, OUTPUT);
    digitalWrite(INP1,LOW);
    digitalWrite(INP2,LOW);
    pwmWrite(ENA, 1000);

	for(;;){
        digitalWrite(INP1,HIGH);
        digitalWrite(INP2,LOW);
        delay(1000);
        digitalWrite(INP1,LOW);
        digitalWrite(INP2,HIGH);
        delay(1000);
	}
	return 0;
}