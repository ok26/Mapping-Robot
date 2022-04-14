import cv2, socket
import numpy as np

cap = cv2.VideoCapture(0)
low_Robot1 = np.array([100,100,100])   #Blue
high_Robot1 = np.array([120,255,255])

low_Robot2 = np.array([140, 40, 2])  #Purple
high_Robot2 = np.array([160, 255, 255])

roomX = 300
roomY = 300
room = np.zeros((roomX,roomY))

s = socket.socket()
s.connect(("192.168.0.119", 5000))