#include <stdio.h>
#include <wiringPi.h>

#define Raindrops_module 2
#define Led 0

int main(void){
	wiringPiSetup();
	pinMode(Raindrops_module, INPUT);
    pinMode(Led, OUTPUT);

	for(;;){
		if(digitalRead(Raindrops_module) == HIGH){
            digitalWrite(Led, HIGH);
            printf("Raindrops_module is not detected\n");
        }
        else{
            digitalWrite(Led, LOW);
            printf("Raindrops_module is detected\n");
        }
        delay(500);
	}
	return 0;
}
