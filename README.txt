For programs to work, you have to install these packages and PIP-libraries:
On RasPi:
	Python
	PIP
		- PIL (Pillow)
		- cv2
		- numpy
		- os
		- time
		- RPi.GPIO
		- paho.mqtt.client
	OpenCV

On server:
	LAMP
	Python
	PIP
		- time
		- mysql.connector
	

Before using these programs, create these two subfolders on RasPi project directory(the same where you place .py-files):
	imgdb		- Used by 1_images.py to collect face images.
	trainer		- Used by 2_trainer.py to save numerical data processed from face images.
