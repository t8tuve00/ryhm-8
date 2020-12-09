import cv2
import os #tarvitaan kuvien tallennukseen
import time

vid = cv2.VideoCapture(0)
vid.set(3, 640)
vid.set(4, 480)

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

pic = 0   # Alustetaan muuttja pic

# Määritä id:t (samat kuin SQL-tauluissa)
idUser = input('\n Enter user ID end press Enter ==>  ')

print("\n Getting things ready. Look at the camera and wait ...")

time.sleep(3)

while(True):

    ret, img = vid.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        pic += 1

        # Tallenna kuvat imgdb-kansioon muodossa "User.[idUser].pic.jpg"
        cv2.imwrite("imgdb/User." + str(idUser) + '.' + str(pic) + ".jpg", gray[y:y+h,x:x+w])

        # cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff
    if k == ord("q"): # keskeytä loop q:lla
        break
    elif pic >= 30: # Ottaa 30 kuvaa ja poistuu
         break

# Sulje ohjelma ja ikkunat
print("\n Exiting Program")
vid.release()
cv2.destroyAllWindows()
