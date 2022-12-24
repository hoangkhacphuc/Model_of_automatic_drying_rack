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
    digitalWrite(ENA, HIGH);
    while (true)
    {
        if (onMotor) {
            digitalWrite(ENA, LOW);
            digitalWrite(IN1, direction ? HIGH : LOW);
            digitalWrite(IN2, direction ? LOW : HIGH);
            cout << "Motor is running\n";
        }
        else {
            digitalWrite(ENA, HIGH);
            cout << "Motor is stop\n";
        }
    }
}

void *button(void *arg) {
    digitalWrite(Led, HIGH);
    for(;;){
		if(digitalRead(Button) == LOW){
            digitalWrite(Led, LOW);
            onMotor = 1;
        }
        else{
            digitalWrite(Led, HIGH);
            onMotor = 0;
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