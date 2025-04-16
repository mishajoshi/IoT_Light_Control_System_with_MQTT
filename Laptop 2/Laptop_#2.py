import paho.mqtt.client as mqtt
import os
import time
from datetime import datetime

# Log file path
LOG_FILE = "mqtt_log.txt"
LED1_LOG_FILE = "led1_timestamps.txt"

# MQTT Topics to Subscribe
TOPICS = ["lightSensor", "threshold", "LightStatus", "Status/RaspberryPiA", "Status/RaspberryPiC"]

# Track LED1 state for logging timestamps
latest_led1_state = None

# Function to log messages to a file
def log_message(topic, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {topic}: {message}\n"
    print(log_entry.strip())  # Print to console

    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)

# Function to log LED1 ON/OFF timestamps
def log_led1_status(status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] LED1 {status}\n"
    
    with open(LED1_LOG_FILE, "a") as led_log:
        led_log.write(log_entry)

# MQTT Connection Callback
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    
    # Subscribe to all required topics with QoS 2
    for topic in TOPICS:
        client.subscribe(topic, qos=2)
        print(f"Subscribed to {topic} with QoS 2")

# MQTT Message Callback
def on_message(client, userdata, msg):
    global latest_led1_state

    message = msg.payload.decode("utf-8")
    log_message(msg.topic, message)

    # Track LED1 state changes
    if msg.topic == "LightStatus":
        if message == "TurnOn" and latest_led1_state != "ON":
            latest_led1_state = "ON"
            log_led1_status("ON")
        elif message == "TurnOff" and latest_led1_state != "OFF":
            latest_led1_state = "OFF"
            log_led1_status("OFF")

# Initialize MQTT Client
client = mqtt.Client()

# Attach Callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(os.getenv('IP'), 1883, 60)

# Keep the client running
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nStopping MQTT client")
