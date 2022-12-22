#include <wiringPi.h>

#define LED 0

int main(void){
	wiringPiSetup();
	pinMode(LED, OUTPUT);
	led(500);
	return 0;
}

void led(int time)
{
    if (time < 0) time = 500;
    while (true){
		digitalWrite(LED,HIGH);
        delay(500);
		digitalWrite(LED,LOW);
        delay(500);
	}
}