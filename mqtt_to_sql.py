import paho.mqtt.client as mqtt
import time
import mysql.connector

def insert_data(idUser):
    sqlcon = mysql.connector.connect(host='localhost',database='lock_info',user='******',password='******')
    query = "INSERT INTO Log(idLog,idUser) VALUES(NULL,%s)" %idUser
    cursor = sqlcon.cursor()
    cursor.execute(query)
    sqlcon.commit()
    cursor.close()
    sqlcon.close()

def on_connect(client, userdata, flags, rc):
    client.subscribe("recog")
 
def on_message(client, userdata, msg):
      msg.payload = msg.payload.decode("utf-8")
      print ("\n------------- RECEIVED DATA-------------")
      print (" MQTT Topic: " + msg.topic )
      print (" Data: " + str(msg.payload))
      insert_data(msg.payload)

mqttHost = "broker.hivemq.com"
mqttPort = 1883
clientName = "SQLserver"
client = mqtt.Client(clientName)
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttHost, mqttPort)

print('---------------------------')
print(' MQTT Receiver Initialized\n Press Ctrl-C to exit')

try:
    client.loop_forever()
except KeyboardInterrupt:
    print(' pressed. Shutting down...')
    print('---------------------------')
