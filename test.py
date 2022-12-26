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
        print(query)
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

class Handler:
    def __init__(self):
        self.database = Database("localhost", "padmin", "12345678", "automatic_drying_rack")
    
    def run(self):
        # lấy dữ liệu trong bảng manager
        manager = self.database.select("manager", ["*"], {})
        # show dữ liệu trong bảng manager
        print(manager)

    def current_time():
        now = datetime.now()
        current = now.strftime("%H:%M:%S")
        return current

    def cleanup(self):
        self.database.cleanup()

if __name__ == "__main__":
    handle = Handler()
    handle.run()