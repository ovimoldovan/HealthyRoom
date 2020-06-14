#include "Arduino.h"
#include "dht.h"
#include "LiquidCrystal.h"
#include <Wire.h>

dht DHT;

#define led 6  //old5
#define DHT11_PIN 7
#define piezopin 6
#define pir 9
#define m 10


const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;


const int trigPin = 3; // old3
const int echoPin = 2; // old2

int counter = 0;
int counter_motion = 0;
int currentState1 = 0;
int previousState1 = 0;
int currentState2 = 0;
int previousState2 = 0;
int inside = 0;
int outside = 0;
int gassensor = A5;

//LiquidCrystal lcd(7, 6, 5, 4, 3, 2);
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
float sensorMQ;
long duration;
int distance;
int value_pir = 0;
int state = LOW;
int a[100];


void setup()
{
	Serial.begin(9600);
	lcd.begin(16, 2);
	lcd.clear();
	pinMode(led, OUTPUT);
	pinMode(trigPin, OUTPUT);
	pinMode(echoPin, INPUT);
	pinMode(piezopin, OUTPUT);
	pinMode(gassensor, INPUT);
	pinMode(value_pir, INPUT);
	pinMode(m, OUTPUT);

}

int toggle = 0;
int k = 0;


void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}

int motor = 0;
void showNewData() {
    if (newData == true) {
        //Serial.println("This just in ... ");
        //lcd.clear();
        //lcd.print("This just in ... ");
        //lcd.print("A");
        //lcd.print(receivedChars);
    	if ((int)receivedChars == 1)
    	{
    		motor = 1;
    	}
    	else
    		motor = 0;

        newData = false;
    }
}


void motor_onoff()
{
	if (motor == 1)
		digitalWrite(m, HIGH);
	else
		digitalWrite(m, LOW);
}





void people_counter()
{
	if ((distance >= 53) && (distance <=55))
		{
		if (toggle>0)
		{
			if (a[0] > a[toggle-1])
			{
				counter++;
			}
			else
			{
				if (counter>0)
				counter--;
			}
		}
		toggle = 0;
		for (int i=0; i<toggle;i++)
		{
			a[i] = 0;
		}
		}
	else if (distance < 53)
		toggle += 1;
	if (toggle>0)
		{
		a[toggle-1]=distance;
		}
//	Serial.print("PERSOANE: ");
//	Serial.println(counter);
}

/*void motion()
{
	value_pir = digitalRead(pir);
		if (value_pir == HIGH)            // check if the sensor is HIGH
		    counter_motion = 10;  // turn LED ON

		else
			counter_motion -= 1;

		if (counter_motion <= 0)
		{
			digitalWrite(led, LOW);
			k = 0;
		}
		else
		{
			digitalWrite(led, HIGH);
			k = 1;
		}
}*/

void loop()
{
	//lcd.clear();
	//dlcd.print("LED1  ON");
	//tone(piezopin, 2000, 500);
	if(Serial.available())
	{
		int r = Serial.parseInt();
		    //Serial.println(r);
		    if (r == 1)
		    {
		    	digitalWrite(led,HIGH);
		    }
		    if (r == 0)
		    {
		    	digitalWrite(led,LOW);
		    }
	}



	digitalWrite(trigPin, LOW);
	delayMicroseconds(2);
	digitalWrite(trigPin, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigPin, LOW);
	duration = pulseIn(echoPin, HIGH);
	distance = (duration/2)/29.1;

	people_counter();
	int chk = DHT.read11(DHT11_PIN);
	int analogSensor = analogRead(gassensor);
	//motion();


	//recvWithEndMarker();
	//showNewData();
//	motor = 1;
//	motor_onoff();
	analogWrite(m, 255);
	//lcd.clear();
	//lcd.print(receivedChars);
	//lcd.setCursor(0, 1);
	//lcd.print("victorie");
	//lcd.setCursor(0, 0);


	Serial.println((String)counter+" "+k+" "+DHT.temperature+" "+DHT.humidity+" "+analogSensor);
	delay(1000);
}
