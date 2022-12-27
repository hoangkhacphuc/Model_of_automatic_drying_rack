import RPi.GPIO as GPIO          
from time import sleep
import mysql.connector
from datetime import datetime
import json

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

# class Button:
#     def __init__(self, pin):
#         self.pin = pin
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#     def is_pressed(self):
#         return GPIO.input(self.pin) == GPIO.HIGH

#     def cleanup(self):
#         GPIO.cleanup()

class LDR_Sensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def is_dark(self):
        return GPIO.input(self.pin) == GPIO.HIGH

    def is_light(self):
        return GPIO.input(self.pin) == GPIO.LOW

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
        self.connection.commit()

    def get(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def cleanup(self):
        self.connection.close()

class Handler:
    def __init__(self):
        self.led = LED(17)
        # self.button = Button(16)
        self.ldr_sensor = LDR_Sensor(23)
        self.raindrop_sensor = Raindrop_Sensor(24)
        self.motor = Motor(25, 5, 6)
        self.database = Database("localhost", "padmin", "12345678", "automatic_drying_rack")
        self.running = False
    
    def run(self):
        self.led.off()
        self.motor.stop()

        while(1):
            if self.ldr_sensor.is_light():
                self.led.on()
                self.database.query("UPDATE `current_status` SET `sunny` = '1' WHERE id = 1")
            else:
                self.led.off()
                self.database.query("UPDATE `current_status` SET `sunny` = '0' WHERE id = 1")

            if self.raindrop_sensor.is_wet():
                self.database.query("UPDATE `current_status` SET `raining` = '1' WHERE id = 1")
            else:
                self.database.query("UPDATE `current_status` SET `raining` = '0' WHERE id = 1")

            current_status = self.database.get("SELECT * FROM `current_status` WHERE id = 1")
            turn_off = current_status[0][4]

            setting = self.database.get("SELECT * FROM `setting`")
            open_time = setting[0][2]
            close_time = setting[1][2]

            open_time = json.loads(open_time)['open']
            close_time = json.loads(close_time)['close']

            a = self.motor.inside
            b = self.check_time(open_time, close_time)
            c = self.raindrop_sensor.is_wet()
            d = self.ldr_sensor.is_light()
            e = turn_off

            if not a and c:
                self.motor.backward()
                self.led.on()
                self.running = True
                sleep(2.5)
                self.motor.stop()
                self.motor.inside = True
                self.led.off()
                self.running = False
                self.database.query("INSERT INTO `history` (`status_id`, `description`) VALUES ('1', 'Trời mưa thu quần áo');")
                self.database.query("UPDATE `current_status` SET `open` = '0' WHERE id = 1")
            elif not a and not b:
                self.motor.backward()
                self.led.on()
                self.running = True
                sleep(2.5)
                self.motor.stop()
                self.motor.inside = True
                self.led.off()
                self.running = False
                self.database.query("INSERT INTO `history` (`status_id`, `description`) VALUES ('1', 'Tới thời gian thu quần áo');")
                self.database.query("UPDATE `current_status` SET `open` = '0' WHERE id = 1")
            elif not a and not d:
                self.motor.backward()
                self.led.on()
                self.running = True
                sleep(2.5)
                self.motor.stop()
                self.motor.inside = True
                self.led.off()
                self.running = False
                self.database.query("INSERT INTO `history` (`status_id`, `description`) VALUES ('1', 'Trời tối thu quần áo');")
                self.database.query("UPDATE `current_status` SET `open` = '0' WHERE id = 1")
            elif not a and b and not c and d and e:
                self.motor.backward()
                self.led.on()
                self.running = True
                sleep(2.5)
                self.motor.stop()
                self.motor.inside = True
                self.led.off()
                self.running = False
                self.database.query("INSERT INTO `history` (`status_id`, `description`) VALUES ('1', 'Thu đồ thủ công');")
                self.database.query("UPDATE `current_status` SET `open` = '0' WHERE id = 1")
            elif a and b and not c and d and not e:
                self.motor.forward()
                self.led.on()
                self.running = True
                sleep(2.5)
                self.motor.stop()
                self.motor.inside = True
                self.led.off()
                self.running = False
                self.database.query("INSERT INTO `history` (`status_id`, `description`) VALUES ('4', 'Thời tiết tốt để đồ');")
                self.database.query("UPDATE `current_status` SET `open` = '1' WHERE id = 1")
            
            # nothing
            sleep(1)
    
    def check_time(self, open, close):
        if len(open) == 5:
            open = open + ":00"
        if len(close) == 5:
            close = close + ":00"

        open = datetime.strptime(open, "%H:%M:%S").time()
        close = datetime.strptime(close, "%H:%M:%S").time()
        now = datetime.now()
        current = now.time()

        if current >= open and current <= close:
            return True
        else:
            return False

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