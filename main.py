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
        self.led = LED(17)
        self.button = Button(16)
        self.ldr_sensor = LDR_Sensor(23)
        self.raindrop_sensor = Raindrop_Sensor(24)
        self.motor = Motor(25, 5, 6)

    def cleanup(self):
        self.led.cleanup()
        self.button.cleanup()
        self.ldr_sensor.cleanup()
        self.raindrop_sensor.cleanup()
        self.motor.cleanup()

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

    def insert(self, table, columns, values):
        query = "INSERT INTO {} ({}) VALUES ({})".format(
            table,
            ", ".join(columns),
            ", ".join(["%s"] * len(values))
        )
        self.cursor.execute(query, values)
        self.connection.commit()

    def select(self, table, columns, conditions):
        query = "SELECT {} FROM {} WHERE {}".format(
            ", ".join(columns),
            table,
            " AND ".join(["{}=%s".format(column) for column in conditions])
        )
        self.cursor.execute(query, tuple(conditions.values()))
        return self.cursor.fetchall()

    def update(self, table, columns, values, conditions):
        query = "UPDATE {} SET {} WHERE {}".format(
            table,
            ", ".join(["{}=%s".format(column) for column in columns]),
            " AND ".join(["{}=%s".format(column) for column in conditions])
        )
        self.cursor.execute(query, tuple(values + list(conditions.values())))
        self.connection.commit()

    def delete(self, table, conditions):
        query = "DELETE FROM {} WHERE {}".format(
            table,
            " AND ".join(["{}=%s".format(column) for column in conditions])
        )
        self.cursor.execute(query, tuple(conditions.values()))
        self.connection.commit()

    def cleanup(self):
        self.connection.close()


# Server API web
class Server:
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.app = Flask(__name__)

    def run(self):
        self.app.run(host=self.host, port=self.port)
    
    # Hàm login để đăng nhập vào hệ thống, lấy access token và trả về json
    @app.route("/login", methods=["POST"])
    def login():
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            result = database.select("manager", ["id", "username", "password"], {"username": username})
            if result:
                user = result[0]
                if user[2] == password:
                    token = jwt.encode({"id": user[0], "username": user[1]})
                    return jsonify({"access_token": token})
                else:
                    return jsonify({"message": "Tài khoản mật khẩu không chính xác"})
            else:
                return jsonify({"message": "Tài khoản không tồn tại"})
        else:
            return jsonify({"message": "Vui lòng nhập đầy đủ thông tin"})

                

if __name__ == "__main__":
    database = Database("localhost", "padmin", "12345678", "automatic_drying_rack")
    server = Server("localhost", 2424, database)
    handler = Handler()
    server.app.run(host=server.host, port=server.port, debug=True)

