#install the library : sudo apt install python3-rpi.gpio

import paho.mqtt.client as mqtt
import os
import RPi.GPIO as GPIO

# GPIO setup
LED1 = 17  # GPIO pin for LED1
LED2 = 27  # GPIO pin for LED2
LED3 = 22  # GPIO pin for LED3

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)

# Initial states
GPIO.output(LED1, GPIO.LOW)
GPIO.output(LED2, GPIO.LOW)
GPIO.output(LED3, GPIO.LOW)

latest_light_status = None  # Track the latest LightStatus message

# Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe("LightStatus")
    client.subscribe("Status/RaspberryPiA")
    client.subscribe("Status/RaspberryPiC")

# Message receiving callback
def on_message(client, userdata, msg):
    global latest_light_status
    
    topic = msg.topic
    message = msg.payload.decode("utf-8")

    if topic == "LightStatus":
        latest_light_status = message
        if message == "TurnOn":
            GPIO.output(LED1, GPIO.HIGH)
        elif message == "TurnOff":
            GPIO.output(LED1, GPIO.LOW)

    elif topic == "Status/RaspberryPiA":
        if message == "online":
            GPIO.output(LED2, GPIO.HIGH)
        elif message == "offline":
            GPIO.output(LED2, GPIO.LOW)

    elif topic == "Status/RaspberryPiC":
        if message == "online":
            GPIO.output(LED3, GPIO.HIGH)
            # Restore LED1 based on the last known LightStatus value
            if latest_light_status == "TurnOn":
                GPIO.output(LED1, GPIO.HIGH)
            elif latest_light_status == "TurnOff":
                GPIO.output(LED1, GPIO.LOW)
        elif message == "offline":
            GPIO.output(LED1, GPIO.LOW)
            GPIO.output(LED3, GPIO.LOW)

client = mqtt.Client()

# Specify callback functions
client.on_connect = on_connect
client.on_message = on_message

# Establish connection
client.connect(os.getenv('IP'), 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting and cleaning up GPIO")
