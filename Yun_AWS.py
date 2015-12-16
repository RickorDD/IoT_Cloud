import json
import paho.mqtt.client as mqtt
import ssl
import serial
import time

#Serialport (Serial1.x) from Yun
ser = serial.Serial('/dev/ttyATH0',57600,timeout=0)

#to begin clear Serialbuffer than during boot YUN send 
#special noc ASCII characters that break message publish
ser.flushInput() 
ser.flush() 

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    ser.write(msg.payload)

def on_log(client, userdata, level, buf):
    print("Log: " + buf)
    
def on_connect(client, userdata, flags, rc):
    client.subscribe("LED")

#Login for AWS IoT
deviceCertificate = "/root/aws/certs/390207a870-certificate.pem.crt"
devicePrivateKey = "/root/aws/certs/390207a870-private.pem.key"
awsCert = "/root/aws/certs/root-CA.crt"
#Topic for message
topic="$aws/things/YUN/shadow/update"
#QOS Level (0,1,2)
qos=0
#Retain when true broker immediately send the messages to new devices 
retain=False
#Clientname
client = mqtt.Client("YUN")

client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

#ssl.PROTOCOL_SSLv23 for Python < 2.7.9 / 3.x
#ssl.PROTOCOL_TLSv1_2 for Python > 2.7.9 / 3.x
client.tls_set(awsCert, deviceCertificate, devicePrivateKey, ssl.CERT_REQUIRED, ssl.PROTOCOL_SSLv23)

#URL for AWS IoT (EU Ireland)
client.connect("A3N80655B02D7L.iot.eu-west-1.amazonaws.com", 8883, 60)

#Client in Loop for subscribed messages and reconnect
client.loop_start()

while True:
    #clear Serialbuffer
    ser.flush()
    
    #read Serialport and remove the String '\n\r' at the end
    Temp=ser.readline().strip('\n\r')
    Hum=ser.readline().strip('\n\r')
    
    #JSON String for AWS IoT
    awsstring = {'state':{ 'reported': {'temperature': Temp,'humidity': Hum }}}
    payload = json.dumps(awsstring)
    
    #Publish message
    client.publish(topic,payload,qos,retain)
    
    time.sleep(300)