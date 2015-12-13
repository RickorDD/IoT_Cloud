#include <DHT.h>

DHT dht(7, DHT22);

unsigned long ul_PreviousMillis = 0UL;
unsigned long ul_Interval = 300000UL;

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
	String incoming = Serial1.readString();
	if(incoming=="ON")
         {
            digitalWrite(9,HIGH);
         }
        if(incoming=="OFF")
         {
            digitalWrite(9,LOW);
         }
}

void sendData()
{
    /*interval Publish Messages*/ 
    
    /*Interval with rollover millis()*/
    unsigned long ul_CurrentMillis = millis();
    if( ul_CurrentMillis - ul_PreviousMillis > ul_Interval)
    {
    ul_PreviousMillis = ul_CurrentMillis;
   	
    /*clear Serialbuffer for actual value*/
    Serial1.flush(); 
    
    Serial1.println(dht.readTemperature());
    Serial1.println(dht.readHumidity());
    }
}