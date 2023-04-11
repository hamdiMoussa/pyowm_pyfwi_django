import pyowm
from .models import weatherrr

owm = pyowm.OWM('your-api-key')

# Search for a city or other location
location = owm.weather_manager().weather_at_place('London,UK')

# Get the current weather conditions
weather = location.weather

# Get the temperature, humidity, and wind speed
temperature = weather.temperature('celsius')['temp']
humidity = weather.humidity
wind_speed = weather.wind()['speed']


post = weatherrr(temp=temperature, hum=humidity, wind=wind_speed)
post.save()