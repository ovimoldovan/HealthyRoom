
import requests, json 
import serial, time

#GET THE CITY NAME FROM OUR SERVER / (FROM API)
serverURL = "http://192.168.43.109:3000/test_get/weather.json"
responseFromServer = requests.get(serverURL, verify=False)
responseObject = responseFromServer.json()
weatherObject = responseObject["weather"]
cityObject = weatherObject["city"]

# USING open weather API to get the weather details
weatherApiKey = "apiKeyHere"
weatherURL = "http://api.openweathermap.org/data/2.5/weather?"
city_name = cityObject
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
    print(" Temperature (in kelvin unit) = " +
                    str(current_temperature) + 
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
          "\n humidity (in percentage) = " +
                    str(current_humidiy) +
          "\n description = " +
                    str(weather_description))
else: 
    print(" City Not Found ")
    

#ARDUINO settings
ser = serial.Serial('/dev/ttyACM0',9600)
ser.flushInput()

#SENDING THE DATA, THAT CAN ALSO BE DONE WITH A WHILE TRUE OR WE HAVE TO SELECT A SAMPLING TIME
s= ser.readline()
s= s.strip()
print (s.decode("utf-8"))
if (s.decode("utf-8") == "<Arduino is ready>"):
    print("sending")
    ans = current_temperature
    ans = ans.encode("utf-8")
    ser.write(ans)
