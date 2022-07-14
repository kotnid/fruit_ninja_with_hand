from re import S
import sqlite3


class database():
    def __init__(self):
        self.conn = sqlite3.connect("data3.db")
        self.c = self.conn.cursor()

    def get(self):
        self.c.execute("SELECT name , score FROM data ORDER BY score DESC")
        result = self.c.fetchall()
        print(result)
        return result

    def add(self , name , score):
        print(score)
        self.c.execute('insert into data(name, score) values (?, ?)', [name , float(score)])
        self.conn.commit()
    
    def find(self , score):
        self.c.execute(f"SELECT count(*) FROM data WHERE score >= {score}")
        result = self.c.fetchone()
        print(result)

        return result
