#API-Key: a-elwo6e-nu40eaf2zb
#Auth-Token: Vzx3cN&_(QxNu-e*Oh

import json
import paho.mqtt.client as mqtt
import ssl
import serial
import time

ser = serial.Serial('/dev/ttyATH0',57600,timeout=0)
ser.flushInput() #clear Serialbuffer
ser.flush() #clear Serialbuffer

org="elwo6e"
username = "use-token-auth"
password = "gyt4_lmsH8c8b1Kc6y" #auth-token
deviceType="YUN"
deviceID="YUN"

topic = "iot-2/evt/status/fmt/json"

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("iot-2/cmd/acommand/fmt/json")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

rootCert = "certs/messaging.pem"

clientID = "d:" + org + ":" + deviceType + ":" + deviceID
client = mqtt.Client(clientID)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password=password)

client.tls_set(ca_certs=rootCert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_SSLv23)

client.connect(org+".messaging.internetofthings.ibmcloud.com", 8883, 60)
client.loop_start() 

while True :
    ser.flush()
    Temp=ser.readline().strip('\n\r')
    Hum=ser.readline().strip('\n\r')
    bluemixstring = {"d":{'temperature': Temp,'humidity': Hum }}
    payload = json.dumps(bluemixstring)
    client.publish(topic, payload, qos=0, retain=False)
    time.sleep(300)