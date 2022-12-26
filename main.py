import RPi.GPIO as GPIO          
from time import sleep
from datetime import datetime

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
        return GPIO.input(self.pin) == GPIO.HIGH

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
        return GPIO.input(self.pin) == GPIO.HIGH

    def is_wet(self):
        return GPIO.input(self.pin) == GPIO.LOW

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
        self.pwm.start(75)
        self.inside = True

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

class Database:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db
        )
        self.cursor = self.connection.cursor()

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def cleanup(self):
        self.connection.close()

class Handler:
    def __init__(self):
        self.led = LED(17)
        self.button = Button(16)
        self.ldr_sensor = LDR_Sensor(23)
        self.raindrop_sensor = Raindrop_Sensor(24)
        self.motor = Motor(25, 5, 6)
        self.database = Database("localhost", "padmin", "12345678", "automatic_drying_rack")
    
    def run(self):
        self.led.off()
        self.motor.stop()

        while(1):
            if self.light_sensor.is_light():
                self.led.on()
                # Cập nhật trạng thái lên database
                self.database.query("UPDATE `current_status` SET `sunny` = '1' WHERE id = 1")
            else:
                self.led.off()
                # Cập nhật trạng thái lên database
                self.database.query("UPDATE `current_status` SET `sunny` = '0' WHERE id = 1")
            sleep(1)

            # if self.motor.inside == false AND self.raindrop_sensor.is_wet():
            #     self.motor.backward()
            #     self.motor.inside = true
            # else:
            #     if self.motor.inside == false AND self.raindrop_sensor.is_dry() AND self.ldr_sensor.is_dark():
            #         self.motor.backward()
            #         self.motor.inside = true
            # else:
            #     if self.motor.inside == true AND self.raindrop_sensor.is_dry() AND self.ldr_sensor.is_light():

    def current_time():
        now = datetime.now()
        current = now.strftime("%H:%M:%S")
        return current

    def cleanup(self):
        self.led.cleanup()
        self.button.cleanup()
        self.ldr_sensor.cleanup()
        self.raindrop_sensor.cleanup()
        self.motor.cleanup()

if __name__ == "__main__":
    handler = Handler()
    try:
        handler.run()
    except KeyboardInterrupt:
        handler.cleanup()