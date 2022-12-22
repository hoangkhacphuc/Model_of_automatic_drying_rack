#include <iostream>
#include <cstdlib>
#include <wiringPi.h>
#include <pthread.h>

#define LED 0
#define LED2 2
#define TIME_LED 500

// void *led()
// {
//     while (true){
// 		digitalWrite(LED,HIGH);
//         delay(TIME_LED);
// 		digitalWrite(LED,LOW);
//         delay(TIME_LED);
// 	}
// }

// void *led2()
// {
//     while (true){
// 		digitalWrite(LED2,HIGH);
//         delay(TIME_LED);
// 		digitalWrite(LED2,LOW);
//         delay(TIME_LED);
// 	}
// }

void *led(void *arg)
{
    while (true){
        digitalWrite(LED,HIGH);
        delay(TIME_LED);
        digitalWrite(LED,LOW);
        delay(TIME_LED);
    }
}

void *led2(void *arg)
{
    while (true){
        digitalWrite(LED2,HIGH);
        delay(TIME_LED);
        digitalWrite(LED2,LOW);
        delay(TIME_LED);
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