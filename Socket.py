import socket 
from threading import Thread 
import time 
import random

class Connection():
    def __init__(self):
        super().__init__()
        self.initSocket()
    
    def initSocket(self):
        self.status = 0
        self.s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        try:
            self.s.bind(('172.16.123.251', 8001))
            print("connected to port 8001")
            self.src_port = 8001
            self.dst_port = 8081

        except:
            self.s.bind(('172.16.123.251', 8081))
            print("connected to port 8081")
            self.s.sendto("handshake".encode(),('172.16.123.251' , 8001))
            self.src_port = 8081
            self.dst_port = 8001
        
        self.score = 0 
        self.recv()

   

    def recv(self):
        while self.status == 0:
            data,addr = self.s.recvfrom(1024)
            
            if data.decode() == "handshake":
                print("recv connection")
                self.s.sendto("handshake_back".encode() , addr)
                break
                
                
            if data.decode() == "handshake_back":
                print("recv recv connection")
                break
    
    def recv2(self):
        self.enemy_marks = "0"
        while True:
                data,addr = self.s.recvfrom(1024)
                if data.decode().split(" ")[0] == "score":
                    self.enemy_marks = data.decode().split(" ")[1]


    def send(self , text):
        self.s.sendto(text.encode(),('172.16.123.251',self.dst_port))

    def mark(self):
        return self.enemy_marks

    def end(self):
        self.status = 1
        
if __name__ == "__main__":
    app = Connection()