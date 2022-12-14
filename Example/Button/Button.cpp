#include <wiringPi.h>

#define Button 2
#define Led 0

int main(void){
	wiringPiSetup();
	pinMode(Button, INPUT);
    pinMode(Led, OUTPUT);

	for(;;){
		if(digitalRead(Button) == 1){
            digitalWrite(Led, HIGH);
        }
        else{
            digitalWrite(Led, LOW);
        }
	}
	return 0;
}