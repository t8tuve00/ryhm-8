import cv2
import numpy as np
import os 

recog = cv2.face.LBPHFaceRecognizer_create()
recog.read('trainer/trainer.yml')
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0 #alustetaan muuttuja "id"

# Id-tunnuksiin kytketyt nimet (Kokeilu, tätä ei välttis tarvita projektissa)
names = ['None', '1', '2', '3', '4'] 

# Käynnistä livevideo
vid = cv2.VideoCapture(0)
vid.set(3, 640) # set video widht
vid.set(4, 480) # set video height

# Tunnistettavien kasvojen minimikoko videolla.
minW = 0.1*vid.get(3)
minH = 0.1*vid.get(4)

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

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, odds = recog.predict(gray[y:y+h,x:x+w])

        # Tarkista todennäköisyys. 0 on 100%:sti tunnistettu.
        if (odds < 100):
            id# = names[id]
            odds = "  {0}%".format(round(100 - odds))
            
        else:
            id = "unknown"
            odds = "  {0}%".format(round(100 - odds))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(odds), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('videra',img) 

    k = cv2.waitKey(10) & 0xff
    if k == ord("q"): # keskeytä q:lla
        break

vid.release()
cv2.destroyAllWindows()