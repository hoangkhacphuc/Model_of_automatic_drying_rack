#include <iostream>
#include <cstdlib>
#include <string>
#include <wiringPi.h>
#include <pthread.h>

#define LED 0
#define TIME_LED 500
#define RAINDROP_SENSOR 2
#define LDR_SENSOR 3

int onLED = 0; // 0 = off, 1 = on

/*
    * Function: initLED
    * ----------------------------
    * Đây là hàm khởi tạo cho led
    * arg: là tham số truyền vào
    * 
    * Hàm này sẽ chạy vô hạn, nếu onLED = 1 thì led sẽ bật và nhấp nháy, ngược lại thì tắt
*/
void *initLED(void *arg) {
    int isHigh = 0;
    while (true){
        if (onLED) {
            digitalWrite(LED,isHigh);
            delay(TIME_LED);
            isHigh = !isHigh;
        }
    }
}

/*
    * Function: isRaining
    * ----------------------------
    * Đây là hàm kiểm tra xem có mưa hay không
    * 
    * Hàm này sẽ trả về 1 nếu có mưa, ngược lại trả về 0
*/

int isRaining() {
    return digitalRead(RAINDROP_SENSOR) == HIGH ? 1 : 0;
}

/*
    * Function: isLight
    * ----------------------------
    * Đây là hàm kiểm tra xem có ánh sáng hay không
    * 
    * Hàm này sẽ trả về 1 nếu có ánh sáng, ngược lại trả về 0
*/

int isLight() {
    return digitalRead(LDR_SENSOR) == HIGH ? 1 : 0;
}

/*
    * Function: handel
    * ----------------------------
    * Đây là hàm xử lý cho chương trình
    * 
    * Hàm này sẽ chạy vô hạn, nếu có mưa hoặc ánh sáng thì bật led, ngược lại thì tắt
*/

void *handel(void *arg) {
    while (true) {
        if (isRaining() || isLight()) {
            onLED = 1;
            cout << "ON" << endl;
        } else {
            onLED = 0;
            cout << "OFF" << endl;
        }
    }
}

/*
    * Function: init
    * ----------------------------
    * Đây là hàm khởi tạo cho chương trình
    * 
    * Hàm này sẽ khởi tạo các chân đầu ra và đầu vào, khởi tạo luồng cho led
*/

void init() {
    wiringPiSetup();

    // Cài đặt chân đầu ra và đầu vào
    pinMode(LED, OUTPUT);
    pinMode(RAINDROP_SENSOR, INPUT);
    pinMode(LDR_SENSOR, INPUT);

    // Tắt led
    digitalWrite(LED, LOW);

    // Khởi tạo luồng cho led
    pthread_t thread1;
    pthread_create(&thread1, NULL, initLED, NULL);
    pthread_join(thread1, NULL);

    // Khởi tạo luồng xử lý chương trình
    pthread_t thread2;
    pthread_create(&thread2, NULL, handel, NULL);
    pthread_join(thread2, NULL);
}

int main(void) {
    init();
	return 0;
}