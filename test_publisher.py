import paho.mqtt.client as mqtt
import os

#Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))

client = mqtt.Client()

# Specify callback function
client.on_connect = on_connect

# Establish a connection
client.connect( os.getenv('IP'), 1883, 160)

# Publish a message
client.publish('lightSensor',payload='Hello Pi 1',qos=1)

client.loop_forever()