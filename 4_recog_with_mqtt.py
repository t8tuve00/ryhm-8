import cv2
import numpy as np
import os
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(5,0)
GPIO.output(18,0)
GPIO.output(27,0)

def on_connect(client, userdata, flags, rc):
    client.subscribe("recog/status")

def on_publish(client, userdata, result):
    print("  MQTT: Data published ")

#MQTT-asetukset
mqttHost = "172.20.240.116"
mqttPort = 1883
clientName = "Raspi"
client = mqtt.Client(clientName)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(mqttHost, mqttPort)

#Kasvontunnistuksen asetukset
recog = cv2.face.LBPHFaceRecognizer_create()
recog.read('trainer/trainer.yml')
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0 #alustetaan muuttuja "id"

names = ['None', '1', '2', '3', '4'] # Id-tunnuksiin kytketyt nimet (Kokeilu, tätä ei välttis tarvita projektissa)

frCounter = 0   #Laskee frameja, ettei lähetä MQTT-viestejä jatkuvasti, kun kasvot havaitaan
msgSend = False
fdCounter = 0
frWaited = False

# Käynnistä livevideon kaappaus
vid = cv2.VideoCapture(0)
vid.set(3, 1024) # kuvan leveys
vid.set(4, 768) # kuvan korkeus
# Tunnistettavien kasvojen minimikoko videolla.
minW = 0.1*vid.get(3)
minH = 0.1*vid.get(4)

def resetIO():
    GPIO.output(5,0)
    GPIO.output(18,0)
    GPIO.output(27,0)

print('---------------------------')
print('Face Recognizer 3.2 running')
print('')
print('Exit with Ctrl-C')

try:
    while True:

        _, img =vid.read()

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        if not msgSend:
            faces = cascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
               )
            
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                id, odds = recog.predict(gray[y:y+h,x:x+w])
                if frWaited:
                    # Tarkista todennäköisyys. 0 on 100%:sti tunnistettu.
                    if (odds < 80):
                        id = names[id]
                        odds = "  {0}%".format(round(100 - odds))
                        print(f'\n- Face recognized. User: {id}  {odds}')
                        ret = client.publish("recog",id)
                        msgSend = True
                        GPIO.output(18,1)
                        GPIO.output(27,1)
                        print('  Lock open')

                    else:
                        # id = "unknown"
                        odds = "  {0}%".format(round(100 - odds))
                        GPIO.output(5,1)
                        print('\n- Unrecognized')
                        print(f'  Prediction: {id}  {odds}')
                        ret = client.publish("recog","unknown")
                        msgSend = True
                
                    cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                    cv2.putText(img, str(odds), (x+5,y+h-5), font, 1, (255,255,0), 1)
                    frWaited = False
                
                else:
                    #Hylkää 3 ensimmäsitä kuvaa kasvontunnistukselta
                    if fdCounter == 13:
                        frWaited = True
                        fdCounter = 0
                    
                    else:
                        fdCounter = fdCounter + 1
        
        else:
            if frCounter == 125:
                GPIO.output(5,0)
                msgSend = False
                frCounter = 0
            
            else:
                frCounter = frCounter + 1

        # cv2.imshow('Video',img)

        if (GPIO.input(17) == 0):
            resetIO()
            print('\n- Lock closed')
            msgSend = False
            frCounter = 0
            time.sleep(2)

        if cv2.waitKey(10) & 0xff == ord("q"): # keskeytä q:lla
            print('Exiting program...')
            break

except KeyboardInterrupt:
    resetIO()
    print(' pressed. Exiting program...')
    print('---------------------------')

    
vid.release()
cv2.destroyAllWindows()
