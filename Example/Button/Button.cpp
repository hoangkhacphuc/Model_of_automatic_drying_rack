#include <iostream>
#include <cstdlib>
#include <string>
#include <wiringPi.h>
#include <pthread.h>

#define Button 29
#define Led 0
#define ENA 6
#define IN1 4
#define IN2 5

using namespace std;
int onMotor = 0; // 0 = off, 1 = on
int direction = 0; // 0 = forward, 1 = backward

// Hàm điều khiển motor theo tốc độ
void *runMotor(void *arg) {
    digitalWrite(ENA, LOW);
    while (true)
    {
        if (onMotor) {
            // Tốc độ motor pwm = 0 -> 100
            // pwmWrite(ENA, 100);

            digitalWrite(ENA, LOW);
            digitalWrite(IN1, direction ? HIGH : LOW);
            digitalWrite(IN2, direction ? LOW : HIGH);
        }
        else {
            digitalWrite(ENA, HIGH);
        }
    }
}

void *button(void *arg) {
    for(;;){
		if(digitalRead(Button) == 1){
            digitalWrite(Led, HIGH);
            onMotor = 1;
            cout << "Button is pressed\n";
        }
        else{
            digitalWrite(Led, LOW);
            onMotor = 0;
            cout << "Button is not pressed\n";
        }
	}
}

int main(void){
	wiringPiSetup();
	pinMode(Button, INPUT);
    pinMode(Led, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);

    // tạo thread cho motor
    pthread_t motorThread, buttonThread;
    pthread_create(&motorThread, NULL, runMotor, NULL);
    pthread_create(&buttonThread, NULL, button, NULL);
    pthread_join(motorThread, NULL);
    pthread_join(buttonThread, NULL);
	return 0;
}