#include <wiringPi.h>

#define Light 3
#define Led 0

int main(void){
	wiringPiSetup();
	pinMode(Light, INPUT);
    pinMode(Led, OUTPUT);

	for(;;){
        int Light_value = digitalRead(Light);

        if(Light_value == HIGH){
            digitalWrite(Led, LOW);
        }
        else{
            digitalWrite(Led, HIGH);
        }
	}
	return 0;
}