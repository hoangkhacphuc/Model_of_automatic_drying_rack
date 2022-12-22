#include <iostream>
#include <cstdlib>
#include <wiringPi.h>
#include <pthread.h>

#define LED 0
#define LED2 2

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

void led2(int time)
{
    if (time < 0) time = 500;
    while (true){
		digitalWrite(LED2,HIGH);
        delay(500);
		digitalWrite(LED2,LOW);
        delay(500);
	}
}

int main(void){
	wiringPiSetup();
	pinMode(LED, OUTPUT);
    pinMode(LED2, OUTPUT);
    pthread_t thread1, thread2;
    pthread_create(&thread1, NULL, led, NULL);
    delay(300);
    pthread_create(&thread2, NULL, led2, NULL);
    pthread_join(thread1, NULL);
    delay(500);
    pthread_join(thread2, NULL);
	return 0;
}