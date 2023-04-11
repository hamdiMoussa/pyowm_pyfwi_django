from .models import Post
from django.shortcuts import render
import pyowm
from .mqtt import start_mqtt_client
import json

import csv 
from .FWI import *
from datetime import datetime

from django.http import HttpResponse, JsonResponse

import os
print(os.getcwd())

#from MQTT_app.mqtt import client as mqtt_client

'''# Create your views here.
def post_list(request):
    posts = Post.objects
    return render(request, 'mqtt/post_list.html', {'posts': posts})'''




def weather(request):
    # Replace "YOUR_API_KEY" with your actual API key from OpenWeatherMap
    owm = pyowm.OWM("0f21fa98b6e075b77fd85b3af087e294")
    
    # Replace "City name" with the name of the city you want weather data for
    location = owm.weather_manager().weather_at_place('Bizerte, TN')
    
    weather = location.weather

    # Get the temperature, humidity, and wind speed
    temperature = weather.temperature('celsius')['temp']
    humidity = weather.humidity
    wind_speed = weather.wind()['speed']
    
    # Create a dictionary of the weather data to pass to the template
    data = {'temperature': temperature, 'humidity': humidity, 'wind': wind_speed}
    
    return render(request, 'mqtt/weather.html', data)


def start_mqtt(request):
    # Start the MQTT client
    start_mqtt_client()
    
    # Return a simple response to indicate that the client has started
    #return HttpResponse('MQTT client started successfully.')
    return render(request, 'mqtt/post_list.html', {})
    


def post_list(request):
    # Retrieve the latest Post object
    #start_mqtt_client()
    post = Post.objects.order_by('-id').first()

    # Render the template and pass the latest Post object as a context variable
    return render(request, 'mqtt/post_list.html', {'post': post})


def getTemp(request):
    TEMP =Post.objects.all()
    return JsonResponse({"TEMP": list(TEMP.values())})



def update_weather(request):
    # Replace "YOUR_API_KEY" with your actual API key from OpenWeatherMap
    owm = pyowm.OWM("0f21fa98b6e075b77fd85b3af087e294")
    
    # Replace "City name" with the name of the city you want weather data for
    location = owm.weather_manager().weather_at_place('Bizerte, TN')
    
    weather = location.weather

    # Get the temperature, humidity, and wind speed
    temperature = weather.temperature('celsius')['temp']
    humidity = weather.humidity
    wind_speed = weather.wind()['speed']
    
    # Create a dictionary of the weather data to pass to the template
    data = {'temperature': temperature, 'humidity': humidity, 'wind': wind_speed}
    # create a dictionary with the updated information
    post = Post(temperature=temperature, humidity=humidity, wind=wind_speed)
    post.save()
    
    # return a JsonResponse with the updated data
    return JsonResponse(data)




def start_FWI(request):

    
    post = Post.objects.order_by('-id').first()
    temperature = post.temperature
    humidity = post.humidity
    wind_speed = post.wind


    with open('testBatch.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.today().strftime('%m/%d/%Y'), temperature, humidity, wind_speed, '5'])


    batchFWI('testBatch.csv')


    with open('testBatch.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        last_row = rows[-1]
        FWI = last_row[-1]
    return render(request, 'mqtt/wfi.html', {'FWI': FWI})



'''def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})'''