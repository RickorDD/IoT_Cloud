#include <ArduinoJson.h>
#include <DHT.h>

DHT dht(7, DHT22);

unsigned long ul_PreviousMillis = 0UL;
unsigned long ul_Interval = 300000UL;
String incoming;

void setup()
{	
    /*for YUN Boot then no Strings from Serialport*/
    delay(60000);  
    
    /*Serial1 is /dev/ttyATH0 at YUN
    for communication edit /etc/inittab
    #ttyATH0::askfirst:/bin/ash --login */
    Serial1.begin(57600);
    
    pinMode(9,OUTPUT);
    dht.begin();
}

void loop()
{
    
  if (Serial1.available() > 0)    
    {
    	recieveData();
    }
    
    sendData();
}


void recieveData()
{
    incoming = Serial1.readString();
    StaticJsonBuffer<200> jsonBuffer;
    JsonObject& root = jsonBuffer.parseObject(incoming);
    int Pin  = root["Pin"].as<int>();
    int State = root["State"].as<int>();
 
    pinMode(Pin,OUTPUT);
 
    if (State==1)
    	{
 	   digitalWrite(Pin,HIGH);
    	}
    if (State==0)
    	{
           digitalWrite(Pin,LOW);
        }
 }

void sendData()
{
    /*interval Publish Messages*/ 
    
    unsigned long ul_CurrentMillis = millis();
    if( ul_CurrentMillis - ul_PreviousMillis > ul_Interval)
    {        
        ul_PreviousMillis = ul_CurrentMillis;
        StaticJsonBuffer<200> jsonBuffer;
        JsonObject& root = jsonBuffer.createObject();
        root["device"] = "YUN";
        root["sensor"] = "DHT22";
        root["temperature"] = dht.readTemperature();
        root["humidity"] = dht.readHumidity();
        root.printTo(Serial1);
    }
}