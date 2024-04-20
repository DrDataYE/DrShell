import sqlite3


class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("./db/modules/modules.db")
        print("Opened database successfully")

    def table(self):
        self.conn.execute(
            """CREATE TABLE COMPANY
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         SALARY         REAL);"""
        )
        print("Table created successfully")

    def execute(self):
        self.conn.execute(
            "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )"
        )
        self.conn.commit()
        print("Records created successfully")

    def close(self):
        self.conn.close()
