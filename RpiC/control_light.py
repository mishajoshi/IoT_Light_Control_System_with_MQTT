import paho.mqtt.client as mqtt

import os

pot_value = -1
ldr_value = -1
decision = ""

#Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    if rc == 0:
        client.subscribe("lightSensor")
        client.subscribe("threshold")
        client.subscribe("LightStatus")
        client.publish("Status/RaspberryPiC","online", qos=2, retain=True)

#Disconnection success callback
def on_disconnect(client, userdata, rc):
    client.publish("Status/RaspberryPiC", "offline", qos=2, retain=True)
    print('Disconnected with result code '+str(rc))

# Message receiving callback
def on_message(client, userdata, msg):
    if msg.topic == "threshold":
        global pot_value
        pot_value = float(msg.payload.decode())
    elif msg.topic == "lightSensor":
        global ldr_value
        ldr_value = float(msg.payload.decode())
    elif msg.topic == "LightStatus":
        global decision
        decision = msg.payload.decode()
    if pot_value >= 0 and ldr_value >= 0 and decision != "":
        if ldr_value >= pot_value and decision != "TurnOff":
            print("Publish Status Off")
            client.publish("LightStatus", "Turnoff", qos=2, retain=True)
        elif ldr_value < pot_value and decision != "TurnOn":
            print("Publish Status On")
            client.publish("LightStatus", "TurnOn", qos=2, retain=True)

client = mqtt.Client()

# Specify callback function
client.will_set("Status/RaspberryPiC", "offline", qos=2, retain=True)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Establish a connection
client.connect(os.getenv('IP'), 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.publish("Status/RaspberryPiC", "offline", qos=2, retain=True)
    client.disconnect()