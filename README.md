# Webcam-Face-Recognition
This is a face recognition system that allows you to categorize people based on their access status, These categories are (Access) and (No Access). Image 1 folder is for people that have access and Image 2 folder is for people that do not have access. If you put the picture of your face in Image 1 folder you will see a green box covering your face on the camera, and if you put it in Image 2 folder, you will see a red box with a text on top that says "FAIL" on it

<table>
  <thead>
    <th>Access</th>
    <th>No Access</th>
  </thead>
  <tbody>
    <tr>
      <td> <img height="239" width="243" src="https://user-images.githubusercontent.com/111835151/186472477-1ecfb7c2-28f5-4b4e-ae55-3345ca214159.gif"></td>
      <td> <img height="239" width="243" src="https://user-images.githubusercontent.com/111835151/186550430-4442c779-ee13-4096-b68f-a201c78eabe1.gif"></td>
    </tr>
  </tbody>
</table>

In this code, the face_recognition library was used to detect faces. Check out their repo for more information. The link is [here](https://github.com/ageitgey/face_recognition). This code can be run on any kind of platform and computer, but for better performance in detections, you need a cuda enabled dlib library. When you try to import face_recognition library it will also import dlib automatically, but it might not be compiled with cuda depending on the system you have and whether or not if cuda is already installed on your computer. 

As can be seen in the table below, there are two different pictures of the same person and even though these pictures were taken in different times and the hair styles are not very similar, the detections and results are very accurate. when the code is exacuted, there will be a number between 0 and 1 that changes constantly and printed on the command prompt. That number is "faceDisAccess" or "faceDisNoAccess". The number is closer to zero, the better the accurracy of the results. 

Here is how they are being calculated;

``` python
   faceDisAccess = face_recognition.face_distance(encodeListAccess, encodeFace)
   faceDisNoAccess = face_recognition.face_distance(encodeListNoAccess, encodeFace)
```

<table>
  <thead>
    <th>Pose 1</th>
    <th>Pose 2</th>
  </thead>
  <tbody>
    <tr>
      <td> <img height="239" width="243" src="https://user-images.githubusercontent.com/111835151/186550430-4442c779-ee13-4096-b68f-a201c78eabe1.gif"></td>
      <td> <img height="239" width="243" src="https://user-images.githubusercontent.com/111835151/186550563-601c2a6e-c59d-477d-977e-e8ef5931c54a.gif"></td>
    </tr>
  </tbody>
</table>

***NOTE: This example includes a pan tilt mechanism and was designed to be used in devices like Raspberry pi or Jetson Nano, but if the code is exacuted on a regular computer, it will still work without any problem, but the camera won't move in the face's direction.***

If you are using a regular computer or do not include servo motors in your project, you can disregard these lines of codes;

``` python
import board
import busio
import os
from adafruit_servokit import ServoKit

i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_pca9685

pwm = adafruit_pca9685.PCA9685(i2c)
pwm.frequency = 50
pwm = ServoKit(channels=16)
pwm.servo[0].angle = 90

x_medium = int(cols / 2)
y_medium = int(cols / 2)
center = int(cols / 2)
position1 = 90

if x_medium < center -70:
    position1 += 3
elif x_medium > center +70:
    position1 -= 3
pwm.servo[0].angle = position1
```

