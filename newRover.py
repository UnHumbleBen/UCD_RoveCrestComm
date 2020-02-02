import cv2
import numpy as np
import socket
import sys
import struct
import base64
import pickle
from threading import Thread
from multiprocessing import Process, Lock


def send_video():
    while True:
        
        ret,frame=cap.read()
        if (ret):
#            lock.acquire()
            encoded, buffer = cv2.imencode('.jpg', frame)
            b_frame = base64.b64encode(buffer)
            b_size = len(b_frame)
                #sending data
            connection.sendall(struct.pack("<L", b_size) + b_frame)
#        lock.release()
            
def recv_cmd():
    while True:
        msg = conn2.recv(1024)
        print(msg.decode("utf-8"))



HOST = ''

cap=cv2.VideoCapture(0)

#lock = Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.bind((HOST, 8000))
s2.bind((HOST, 1235))


s.listen(1)
s2.listen(1)

print("Ready to connect")
connection, addr = s.accept()

conn2, addr2 = s2.accept()

print (addr)
print (addr2)

#
#send_video()
#recv_cmd()


proc1 = Thread(target=send_video)
proc2 = Thread(target=recv_cmd)

proc1.start()
proc2.start()
