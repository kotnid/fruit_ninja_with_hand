from re import S
import sqlite3


class database():
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.c = self.conn.cursor()

    def get(self):
        self.c.execute("SELECT name , score FROM data ORDER BY score DESC LIMIT 20")
        result = self.c.fetchall()
        print(result)
        return result

    def add(self , name , score):
        print(score)
        self.c.execute('insert into data(name, score) values (?, ?)', [name , float(score)])
        self.conn.commit()
        
