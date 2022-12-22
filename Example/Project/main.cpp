#include <iostream>
#include <cstdlib>
#include <string>
#include <wiringPi.h>
#include <pthread.h>

#define LED 0
#define LED_STATUS 1
#define TIME_LED 500

#define RAINDROP_SENSOR 2
#define LDR_SENSOR 3
#define BTN_STATUS 4


using namespace std;

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
    
    // Tắt led
    digitalWrite(LED, LOW);
    digitalWrite(LED_STATUS, LOW);

    while (true){
        if (onLED) {
            digitalWrite(LED,isHigh);
            delay(TIME_LED);
            isHigh = !isHigh;
        }
        else {
            digitalWrite(LED,LOW);
        }
    }
}

/*
    * Function: ledStatus
    * ----------------------------
    * Đây là hàm bật led thống báo trạng thái bật/tắt của hệ thống
    * status = 0: tắt led
    * status = 1: bật led
    * 
    * Hàm này sẽ bật/tắt led theo status
*/

void ledStatus(int status) {
    digitalWrite(LED, status);
}

/*
    * Function: isRaining
    * ----------------------------
    * Đây là hàm kiểm tra xem có mưa hay không
    * 
    * Hàm này sẽ trả về 1 nếu có mưa, ngược lại trả về 0
*/
int isRaining() {
    return digitalRead(RAINDROP_SENSOR) == LOW ? 1 : 0;
}

/*
    * Function: isLight
    * ----------------------------
    * Đây là hàm kiểm tra xem có ánh sáng hay không
    * 
    * Hàm này sẽ trả về 1 nếu có ánh sáng, ngược lại trả về 0
*/
int isLight() {
    return digitalRead(LDR_SENSOR) == LOW ? 1 : 0;
}

/*
    * Function: handel
    * ----------------------------
    * Đây là hàm xử lý cho chương trình
    * 
    * Hàm này sẽ chạy vô hạn, nếu có mưa hoặc ánh sáng thì bật led, ngược lại thì tắt
*/
void *handel(void *arg) {
    cout << "Start handel\n";
    while (true) {
        if (isRaining() || isLight()) {
            onLED = 1;
        } else {
            onLED = 0;
        }
        // Nếu nhấn nút thì bật led thống báo trạng thái
        if (digitalRead(BTN_STATUS) == LOW) {
            ledStatus(1);
        }
        else {
            ledStatus(0);
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
    pinMode(LED_STATUS, OUTPUT);
    pinMode(RAINDROP_SENSOR, INPUT);
    pinMode(LDR_SENSOR, INPUT);
    pinMode(BTN_STATUS, INPUT);

    // Khởi tạo luồng cho led
    pthread_t thread1, thread2;
    pthread_create(&thread1, NULL, initLED, NULL);
    pthread_create(&thread2, NULL, handel, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
}

int main(void) {
    cout << "Start\n";
    init();
	return 0;
}