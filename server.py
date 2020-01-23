import socket
import time

import cv2

capture = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sock.gethostname(), 1234))

while True:
    ret, frame = capture.read()
    data = cv2.imencode('.jpg', frame)[1].tostring()
    sock.sendall(data)
    time.sleep(2)
