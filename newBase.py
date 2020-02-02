import socket
import struct
import base64
import cv2
import datetime
import numpy as np
import pickle
from tkinter import *
from threading import Thread
import concurrent.futures
from multiprocessing import Process, Lock


def video_stream():
    payload_size = struct.calcsize("<L")
    data = b''
    while(True):
        start_time = datetime.datetime.now()
        while len(data) < payload_size:
            data += s_vid1.recv(4096)
        frame_size = struct.unpack("<L", data[:payload_size])[0]
        data = data[payload_size:]
        while len(data) < frame_size:
            data += s_vid1.recv(131072)
        frame_data = data[:frame_size]
        data = data[frame_size:]
        img = base64.b64decode(frame_data)
        npimg = np.frombuffer(img, dtype=np.uint8)
        frame = cv2.imdecode(npimg, 1)

        #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        end_time = datetime.datetime.now()
        fps = 1/(end_time-start_time).total_seconds()
        print("Fps: ",round(fps,2))

        # Display
        cv2.imshow('frame', frame)
        
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break;

def send_cmd():
    s_cmd1.send(bytes("hello", "utf-8"))


master = Tk()

s_vid1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s_cmd1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s_vid1.connect(('localhost',8000))
s_cmd1.connect(('localhost',1235))


b2 = Button(master, text="video", command=video_stream)
b2.place(relx=0.67, rely=0.25, anchor=CENTER)

b2 = Button(master, text="hello", command=send_cmd)
b2.place(relx=0.33, rely=0.25, anchor=CENTER)



mainloop()
