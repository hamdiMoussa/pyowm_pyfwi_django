
import json
from .models import Post

import paho.mqtt.client as mqtt
from django.conf import settings


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('v3/loraatest02@ttn/devices/eui-70b3d57ed005a5c4/up')
    else:
        print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    # Decode the incoming message
    payload_dict =json.loads(msg.payload)
   # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

    # Get temperature and humidity values from payload
    temperature = payload_dict['uplink_message']['decoded_payload']['temperature']
    humidity = payload_dict['uplink_message']['decoded_payload']['humidity']
    print('temperature :', temperature, 'humidity :', humidity,'\n')

    # Create a new Post object and save it to the database
    post = Post(temperature=temperature, humidity=humidity)
    post.save()

def start_mqtt_client():
    # Create a new MQTT client instance
    client = mqtt.Client()

    # Set the client's connection and message handling functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Set the client's username and password
    client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

    # Connect to the MQTT broker
    client.connect(
        host=settings.MQTT_SERVER,
        port=settings.MQTT_PORT,
        keepalive=settings.MQTT_KEEPALIVE
    )

    # Start the MQTT loop (this function blocks and waits for incoming messages)
    client.loop_forever()