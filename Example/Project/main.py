import RPi.GPIO as GPIO          
from time import sleep

class LED:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def blink(self, times, delay):
        for i in range(times):
            self.on()
            sleep(delay)
            self.off()
            sleep(delay)

    def cleanup(self):
        GPIO.cleanup()

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_pressed(self):
        print('Pressed\n')
        return GPIO.input(self.pin) == GPIO.LOW

    def cleanup(self):
        GPIO.cleanup()

class LDR_Sensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def is_dark(self):
        return GPIO.input(self.pin) == GPIO.LOW

    def is_light(self):
        return GPIO.input(self.pin) == GPIO.HIGH

    def cleanup(self):
        GPIO.cleanup()

class Raindrop_Sensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def is_dry(self):
        return GPIO.input(self.pin) == GPIO.LOW

    def is_wet(self):
        return GPIO.input(self.pin) == GPIO.HIGH

    def cleanup(self):
        GPIO.cleanup()
    
class Motor:
    def __init__(self, ena, pin1, pin2):
        self.ena = ena
        self.pin1 = pin1
        self.pin2 = pin2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        self.pwm = GPIO.PWM(self.ena, 1000)
        self.pwm.start(25)

    def forward(self):
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.LOW)

    def backward(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()

class Handler:
    def __init__(self):
        self.led = LED(11)
        self.button = Button(24)
        self.ldr_sensor = LDR_Sensor(16)
        self.raindrop_sensor = Raindrop_Sensor(18)
        self.motor = Motor(22, 29, 31)

    def cleanup(self):
        self.led.cleanup()
        self.button.cleanup()
        self.ldr_sensor.cleanup()
        self.raindrop_sensor.cleanup()
        self.motor.cleanup()

if __name__ == "__main__":
    handler = Handler()
    try:
        while True:
            if handler.button.is_pressed():
                handler.led.on()
            else:
                handler.led.off()
            if handler.ldr_sensor.is_dark():
                handler.motor.forward()
            else:
                handler.motor.stop()
            if handler.raindrop_sensor.is_wet():
                handler.motor.backward()
            else:
                handler.motor.stop()
    except KeyboardInterrupt:
        handler.cleanup()