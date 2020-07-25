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
            conn_vid1.sendall(struct.pack("<L", b_size) + b_frame)
#        lock.release()
            
def recv_cmd():
    while 1:
        msg = conn_cmd1.recv(1024)
        print("recieved command " + str(msg.decode("utf-8")))



HOST = ''

cap=cv2.VideoCapture(0)

#lock = Lock()

s_vid1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_cmd1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s_vid1.bind((HOST, 8000))
s_cmd1.bind((HOST, 1235))


s_vid1.listen(5)
s_cmd1.listen(5)

print("Ready to connect")

conn_vid1, addr_vid1 = s_vid1.accept()
conn_cmd1, addr_cmd1 = s_cmd1.accept()

print (addr_vid1,addr_cmd1)



#start runninng with multithread
proc1 = Thread(target=send_video)
proc2 = Thread(target=recv_cmd)

proc1.start()
proc2.start()
