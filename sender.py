import cv2
import numpy as np
import socket
import sys
import pickle
import struct

cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',1234))

while True:
    ret,frame=cap.read()

    data = pickle.dumps(frame)

    # message length
    message_size = struct.pack("L", len(data)) ### CHANGED

    # data
    clientsocket.sendall(message_size + data)
