import socket
import cv2
import numpy as np
import time

HOST = '192.168.1.10'
PORT = 50505

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((socket.gethostname(), 1234))
print('Socket bind complete')

s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

while True:
    data = conn.recv(8192)
    nparr = np.fromstring(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow('frame', frame)
    time.sleep(2)
