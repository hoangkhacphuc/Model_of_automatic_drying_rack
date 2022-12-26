from time import sleep
from datetime import datetime
import mysql.connector

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

    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def cleanup(self):
        self.connection.close()

class Handler:
    def __init__(self):
        self.database = Database("localhost", "padmin", "12345678", "automatic_drying_rack")
    
    def run(self):
        manager = self.database.select("SELECT * FROM `manager`")
        # in ra name tất cả
        print(manager.name)

    def current_time():
        now = datetime.now()
        current = now.strftime("%H:%M:%S")
        return current

    def cleanup(self):
        self.database.cleanup()

if __name__ == "__main__":
    handle = Handler()
    handle.run()