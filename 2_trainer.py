import cv2
import numpy as np
from PIL import Image
import os

# Kuvakansio
path = 'imgdb'

recog = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

# Funktio muuntaa vertailukuvat numeeriseksi dataksi
def imgsLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

print ("\n Training faces. Wait for a few seconds...")
faces,ids = imgsLabels(path)
recog.train(faces, np.array(ids))

# Tallenna tiedosto trainer kansioon
recog.write('trainer/trainer.yml')

# Tulosta opeteltujen kasvojen lkm ja poistu
print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))