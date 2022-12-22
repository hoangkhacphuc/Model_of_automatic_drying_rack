#include <wiringPi.h>

#define Raindrops_module 2
#define Led 0

int main(void){
	wiringPiSetup();
	pinMode(Raindrops_module, INPUT);
    pinMode(Led, OUTPUT);

	for(;;){
        int Raindrops_module_value = digitalRead(Raindrops_module);

        if(Raindrops_module_value == HIGH){
            digitalWrite(Led, LOW);
        }
        else{
            digitalWrite(Led, HIGH);
        }
	}
	return 0;
}