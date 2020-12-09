import cv2
import numpy as np
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(5,0)
GPIO.output(18,0)
GPIO.output(27,0)


# import lock

recog = cv2.face.LBPHFaceRecognizer_create()
recog.read('trainer/trainer.yml')
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0 #alustetaan muuttuja "id"
# Id-tunnuksiin kytketyt nimet (Kokeilu, tätä ei välttis tarvita projektissa)
names = ['None', '1', '2', '3', '4'] 

# Käynnistä livevideon kaappaus
vid = cv2.VideoCapture(0)
vid.set(3, 640) # kuvan leveys
vid.set(4, 480) # kuvan korkeus
# Tunnistettavien kasvojen minimikoko videolla.
minW = 0.1*vid.get(3)
minH = 0.1*vid.get(4)

def face_detect():
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

    id, odds = recog.predict(gray[y:y+h,x:x+w])

    # Tarkista todennäköisyys. 0 on 100%:sti tunnistettu.
    if (odds < 70):
        id #= names[id]
        odds = "  {0}%".format(round(100 - odds))
        
        # time.sleep(2)
        # GPIO.output(18,0)
        # GPIO.output(27,0)
        
        # open_lock()
        
        GPIO.output(18,1)
        GPIO.output(27,1)
        print(f'-Face recognized. User: {id}')
        print('Lock open')
        
        

    else:
        id = "unknown"
        odds = "  {0}%".format(round(100 - odds))
        unknown()

    
    cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
    cv2.putText(img, str(odds), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
def reset():
    GPIO.output(5,0)
    GPIO.output(18,0)
    GPIO.output(27,0)
    
# def open_lock():
    # GPIO.output(18,1)
    # GPIO.output(27,1)
    # print(f'-Face recognized. User: {id}. Lock opened.')
    # while not GPIO.input(17):
        # time.sleep(0.1)
        # # if (GPIO.input(17) == 0):
            # # reset()

def unknown():
    GPIO.output(5,1)
    print('*Unrecognized person*')
    # time.sleep(2)
    GPIO.output(5,0)

print('---------------------------')
print('Face Recognizer 3.2 running')
print('')
print('Exit with Ctrl-C')

try:
    while True:

        ret, img =vid.read()

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = cascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 13,
            minSize = (int(minW), int(minH)),
           )
        
            
        for(x,y,w,h) in faces:
            face_detect()
            
            

    #    img = cv2.rotate(img, 1)    
        cv2.imshow('Video',img)

        if (GPIO.input(17) == 0):
            reset()
            print('-Lock closed')
            time.sleep(5)
            

<<<<<<< HEAD
        if cv2.waitKey(10) & 0xff == ord("q"): # keskeytä q:lla
            print('Exiting program...')
            break
=======
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(odds), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('Video',img) 
>>>>>>> 91ee715b7370ac53e5141abd2f6d4b16f0b65a57

except KeyboardInterrupt:
    reset()
    print(' pressed. Exiting program...')
    print('---------------------------')

    
vid.release()
cv2.destroyAllWindows()
<<<<<<< HEAD
=======

>>>>>>> 91ee715b7370ac53e5141abd2f6d4b16f0b65a57
