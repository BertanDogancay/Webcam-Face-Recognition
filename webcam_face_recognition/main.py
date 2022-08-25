from typing import ClassVar
import cv2
from face_recognition.api import compare_faces, face_distance
import numpy as np
import face_recognition
import board
import busio
import os
from adafruit_servokit import ServoKit
from datetime import datetime

i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_pca9685

pwm = adafruit_pca9685.PCA9685(i2c)
pwm.frequency = 50
pwm = ServoKit(channels=16)
pwm.servo[0].angle = 90

path = '/your path to first images1 folder which is allowed faces'
images1 = []
images2 = []
classNames = []
classNamesA = []
mylist = os.listdir(path)

for cls in mylist:
    curImg = cv2.imread(f'{path}/{cls}')
    images1.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
    
def findEncodings(images1):
    encodeList = []
    for img in images1:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListAccess = findEncodings(images1)
print('Encoding1 Complete')

path = '/your path to first images2 folder which is denied faces'
mylistA = os.listdir(path)
for cl in mylistA:
    curImg = cv2.imread(f'{path}/{cl}')
    images2.append(curImg)
    classNamesA.append(os.path.splitext(cl)[0])

def findEncodings(images2):
    encodeList = []
    for img in images2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode2 = face_recognition.face_encodings(img)[0]
        encodeList.append(encode2)
    return encodeList

encodeListNoAccess = findEncodings(images2) 
print('Encoding2 Complete')

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
rows, cols, _= frame.shape

x_medium = int(cols / 2)
y_medium = int(cols / 2)
center = int(cols / 2)
position1 = 90

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matchesAccess = face_recognition.compare_faces(encodeListAccess, encodeFace)
        faceDisAccess = face_recognition.face_distance(encodeListAccess, encodeFace)
        matchesNoAccess = face_recognition.compare_faces(encodeListNoAccess, encodeFace)
        faceDisNoAccess = face_recognition.face_distance(encodeListNoAccess, encodeFace)
        matchIndexA = np.argmin(faceDisAccess)
        matchIndexNA = np.argmin(faceDisNoAccess)

        if matchesAccess[matchIndexA]:
            name = classNames[matchIndexA].upper() 
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            print(faceDisAccess)
            x_medium = int((x1+x2)/2)
            y_medium = int((y1+y2)/2)
            
            cv2.putText(img,'success',(x1+8,y1-10),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.rectangle(img, (x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

        if matchesNoAccess[matchIndexNA]:
            name = classNamesA[matchIndexNA].upper() 
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            markTime(name)
            print(faceDisNoAccess)
            x_medium = int((x1+x2)/2)
            y_medium = int((y1+y2)/2)

            cv2.putText(img,'FAIL',(x1+30,y1-10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            cv2.rectangle(img, (x1,y1),(x2,y2),(0,0,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                


    cv2.imshow('Webcam', img)
    key = cv2.waitKey(1)

    if key == 27:
        break
    
    if x_medium < center -70:
        position1 += 3
    elif x_medium > center +70:
        position1 -= 3
    pwm.servo[0].angle = position1
    
cap.release()
cv2.destroyAllWindows()
