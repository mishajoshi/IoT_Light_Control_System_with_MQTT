import smbus
import time
import paho.mqtt.client as mqtt
import os

# Initialize I2C
bus = smbus.SMBus(1)  # Use I2C bus 1 on Raspberry Pi
ADS7830_ADDRESS = 0x48  # Default I2C address of ADS7830
prev_light = 0
prev_pot = 0


#Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+ str(rc))
    if rc == 0:
        client.subscribe("lightSensor")
        client.subscribe("threshold")
        client.publish("Status/RaspberryPiA", "online", qos=2, retain=True)

#Disconnection success callback
def on_disconnect(client, userdata, rc):
    client.publish("Status/RaspberryPiA", "offline", qos=2, retain=True)
    print('Disconnected with result code '+ str(rc))

def translate_address(channel):
    a = channel & 0b100
    b = channel & 0b010
    c = channel & 0b001
    channel = (c << 2) | (a >> 1) | (b >> 1)
    return 128 | (channel << 4)

def on_message(client, userdata, msg):
    if msg.topic == "threshold":
        global prev_pot
        prev_pot = float(msg.payload.decode())
    elif msg.topic == "lightSensor":
        global prev_light
        prev_light = float(msg.payload.decode())

client = mqtt.Client()

client.will_set("Status/RaspberryPiA", "offline", qos=2, retain=True)
# Specify callback function
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Establish a connection
client.connect( os.getenv('IP'), 1883, 60) 
client.loop_start()

light_threshold = 0.35
pot_threshold = 0.25

client.on_message = on_message

try:
    while True:
        if prev_light >= 0:
            # Read LDR on channel 0
            ldr_value = bus.read_byte_data(ADS7830_ADDRESS, translate_address(6))/255
             # Publish a message
            if abs(ldr_value - prev_light) > light_threshold:
                print(f'LightSensor Publish {ldr_value}')
                client.publish('lightSensor',payload=ldr_value,qos=2, retain=True)
                prev_light = ldr_value
        
        if prev_pot >= 0:
            # Read Potentiometer on channel 1
            pot_value = bus.read_byte_data(ADS7830_ADDRESS, translate_address(7))/255
        
            if abs(pot_value - prev_pot) > pot_threshold:
                print(f'Pot Publish {pot_value}')
                client.publish('threshold',payload=pot_value,qos=2, retain=True)
                prev_pot = pot_value
            
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nExiting...")
    on_disconnect(client, None, 0)
    client.disconnect()
except Exception as e:
    print(f"Error:{e}") 