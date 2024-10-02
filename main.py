import requests
import math
import smtplib
from datetime import datetime

my_email = "carduibot@gmail.com"
password = "ydffosgveywfvfrr"

MY_LAT = 21.832350
MY_LONG = -102.317330

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

iss_longitude = float(data["iss_position"]["longitude"])
iss_latitude = float(data["iss_position"]["latitude"])

iss_position = (iss_longitude, iss_latitude)

print(iss_position)

lat_closeness = math.isclose(MY_LAT, iss_latitude, abs_tol = 50)
lng_closeness = math.isclose(MY_LONG, iss_longitude, abs_tol = 50)

if lat_closeness and lng_closeness == True:
    location_closeness = True
else:
    location_closeness = False

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

sunrise_hour = data["results"]["sunrise"].split("T")[1].split(":")[0]
sunrise_minute = data["results"]["sunrise"].split("T")[1].split(":")[1]
sunset_hour = data["results"]["sunset"].split("T")[1].split(":")[0]
sunset_minute = data["results"]["sunset"].split("T")[1].split(":")[1]

print(f"sunrise: {sunrise_hour}:{sunrise_minute}\nsunset: {sunset_hour}:{sunset_minute}")

time_now = datetime.now()
now_hour = str(time_now).split(" ")[1].split(":")[0]
now_minute = str(time_now).split(" ")[1].split(":")[1]

print(f"{now_hour}:{now_minute}")

night_time = False
if int(sunset_hour) <= int(now_hour) <= int(sunrise_hour):
    night_time = True

if location_closeness and night_time:
    print("ISS is close to you")

    message = f"""Dear Ms. Stark,
    The International Space Station is moving at close to your location (home) at the moment.
    Keep in mind that it moves close to 28,000 km/h, so look up quickly!
    
    The current ISS position is {iss_position}
    Right now's time: {now_hour}:{now_minute}
    Today's night:
        Sunrise: {sunrise_hour}:{sunrise_minute}
        Sunset: {sunset_hour}:{sunset_minute}
    
    Your loyal buddy,
    CarduiBot
    """

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email,
                        to_addrs="vanessa@reteguin.com",
                        msg=f"Subject:ISS is close to you!\n\n{message}")
    connection.close()
    print("Notification sent successfully")

