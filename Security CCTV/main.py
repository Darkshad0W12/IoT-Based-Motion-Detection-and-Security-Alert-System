import serial.tools.list_ports 
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import cv2
from cv2 import VideoCapture
from cv2 import imshow
from cv2 import imwrite
from cv2 import destroyAllWindows
from cv2 import destroyWindow

a=time.time()
ports =serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList= []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val= input("Select port: COM")
print(val)

portVar=""

for x in range(0,len(portList)):
    if(portList[x].startswith("COM"+str(val))):
        portVar = "COM"+str(val)
        print(portList[x])

serialInst.baudrate = 9600
serialInst.port= portVar
serialInst.open()

flag=0
start=int(time.time())
def SendMail(ImgFileName):
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'Security alert !'
    msg['From'] = '**********************'
    msg['To'] = '*****************'
    UserName="**************"
    UserPassword="**************"
    text = MIMEText("Motion detected !")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)
    s = smtplib.SMTP_SSL("smtp.gmail.com",465)
    s.login(UserName, UserPassword)
    s.sendmail("*************","************", msg.as_string())
    s.quit()
                
while True:
    if(serialInst.in_waiting):
        packet = serialInst.readline()
        pkt=int(packet.decode('utf'))
        if(pkt<27):
            flag=1
            #add img campture and mail...
            cam=VideoCapture(1)
            result, image=cam.read()
            if (result):
                imshow("img",image)
                imwrite("img.png",image)
                destroyWindow("img")

            SendMail("img.png")
        if(flag==1):
            a=time.time()
            import cv2
            #Capture video from webcam
            vid_capture = cv2.VideoCapture(1)
            vid_cod = cv2.VideoWriter_fourcc(*'mp4v')
            output = cv2.VideoWriter(f"C:\\Users\\ANURAAG\\Videos\\{a}.mp4", vid_cod, 30.0, (640,480))
            start=int(time.time())
            while(flag==1):
                # Capture each frame of webcam video
                ret,frame = vid_capture.read()
                cv2.imshow("My cam video", frame)
                output.write(frame)
                # Close and break the loop after pressing "x" key
                if cv2.waitKey(1) &0XFF == ord('x'):
                    flag=0
                end=start+30
                if int(time.time())== end:
                    if(serialInst.in_waiting):
                        packet = serialInst.readline()
                        pkt=int(packet.decode('utf'))
                        if(pkt<27):
                            flag=1
                            print("obj still present:")
                            start=int(time.time())
                        else:
                            flag=0
                            print("obj not present:")
                            destroyWindow("My cam video")
                            #start=int(time.time())
            # close the already opened camera
            vid_capture.release()
            # close the already opened file
            output.release()
            # close the window and de-allocate any associated memory usage
            cv2.destroyAllWindows()
