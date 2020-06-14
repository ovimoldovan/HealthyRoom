import requests, json
import serial
import time
import threading
from threading import Thread

roomName = "Room1"
ventState = 0
restHeader = {"Content-Type": "application/json"}

def getCityNameFromUserInterface():
    serverURL = "http://192.168.43.109:3000/test_get/weather.json"
    responseFromServer = requests.get(serverURL, verify=False)
    responseObject = responseFromServer.json()
    weatherObject = responseObject["weather"]
    cityObject = weatherObject["city"]
    return cityObject

def getWeatherDetailsFromWebAsObject():
    weatherApiKey = "apiKeyHere"
    weatherURL = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = getCityNameFromUserInterface()
    complete_url = weatherURL + "appid=" + weatherApiKey + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    #404 means that city is not found
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]  #that's in kelvin
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        #print(" Temperature (in kelvin unit) = " +
        #                str(current_temperature) +
        #      "\n atmospheric pressure (in hPa unit) = " +
        #                str(current_pressure) +
        #      "\n humidity (in percentage) = " +
        #                str(current_humidiy) +
        #      "\n description = " +
        #                str(weather_description))
    else:
        print(" City Not Found ")
    return y

def getOutsideTemperature():
    y = getWeatherDetailsFromWebAsObject()
    return y["temp"]

def sendToArduino(sendString):
    ser = serial.Serial('/dev/ttyACM0',9600)
    ser.flushInput()
    s= ser.readline()
    s= s.strip()
    print (s.decode("utf-8"))
    if (s.decode("utf-8") == "<Arduino is ready>"):
        print("sending")
        ans = sendString
        ans = ans.encode("utf-8")
        ser.write(ans)
        
def test():
    i = 0
    while True:
        sendToArduino(str(i))
        i+=1
        time.sleep(1000)
        print(i)

def changeVentState():
    serverURL = "http://192.168.43.109:3000/test_get/weather.json"
    responseFromServer = requests.get(serverURL, verify=False)
    responseObject = responseFromServer.json()
    ventObject = responseObject["ventState"]
    if ventObject == "on":
        ventState = 1
        sendToArduino("VentOn")
    else:
        ventState = 0
        sendToArduino("VentOff")
        
def updatePresenceSituation():
    ser = serial.Serial('/dev/ttyACM0',9600)
    ser.flushInput()
    s= ser.readline()
    s= s.strip()
    print (s.decode("utf-8"))
    if (s.decode("utf-8") == "Motion detected"):
        data = {"people":"yes"}
        print("prezenta")
        time.sleep(1000) 
    if(s.decode("utf-8") == "No motion detected"):
        data = {"people":"no"}
        print("nu-i prezenta")
        time.sleep(1000) 
     
    serverURL = "http://192.168.43.109:3000/test_get/weather.json"
    
    #responseFromServer = requests.put(serverURL, data = json.dump(data), headers = restHeader)

def ventThread():
    while(True):
        responseFromServer = requests.get(url = "http://192.168.43.109:3000/rooms/6/get_fan_status", verify=False)
        responseObject = responseFromServer.json()
        ventObject = responseObject["ventState"] 
        print(ventObject)
        time.sleep(1000)
        if(ventState == "off"):
            sendToArduino("0")
        else:
            sendToArduino("1")
            

def main():
    #outsideTemperature = getOutsideTemperature()
    #sendToArduino(str(outsideTemperature))
    #print(outsideTemperature)
    #test()
    ser = serial.Serial('/dev/ttyACM0',9600)
    serverURL = "http://192.168.43.109:3000/rooms/6/get_fan_status"
    while(True):
        ser.flushInput()
        s= ser.readline()
        s= s.strip()
        print (s.decode("utf-8"))
        fullData = (s.decode("utf-8")).split()
        counterPeople = fullData[0] #int
        motionDetected = fullData[1] #1 = exista miscare, 0 = nu exista
        temperatureInside = fullData[2] #float
        humidityInside = fullData[3] #float
        gasData = fullData[4] #int
        
        print(motionDetected)
        
        #time.sleep(500)
        
        #outsideTemperature = getOutsideTemperature()
        ans = "1"
        ans = ans.encode("utf-8")
        ser.write(ans)
        
        
    
#main()
        
class ventClass(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            responseFromServer = requests.get(url = "http://192.168.43.109:3000/rooms/6/get_fan_status", verify=False)
            responseObject = responseFromServer.json()
            ventObject = responseObject["ventState"] 
            print(ventObject)
            time.sleep(1)
            
class mainClass(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        ser = serial.Serial('/dev/ttyACM0',9600)
        serverURL = "http://192.168.43.109:3000/rooms/6/get_fan_status"
    def run(self):
        while True:
            ser.flushInput()
            s= ser.readline()
            s= s.strip()
            print (s.decode("utf-8"))
            fullData = (s.decode("utf-8")).split()
            counterPeople = fullData[0] #int
            motionDetected = fullData[1] #1 = exista miscare, 0 = nu exista
            temperatureInside = fullData[2] #float
            humidityInside = fullData[3] #float
            gasData = fullData[4] #int
            
            print(motionDetected)
            
            #time.sleep(500)
            
            #outsideTemperature = getOutsideTemperature()
            ans = "1"
            ans = ans.encode("utf-8")
            ser.write(ans)


ventClass()
#mainClass()
while(True):
    pass

