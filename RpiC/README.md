
# Raspberry Pi MQTT Light Control

This project uses a Raspberry Pi to control a light based on readings from an LDR (Light Dependent Resistor) and a potentiometer. It listens for sensor values via MQTT and makes decisions to turn the light on or off accordingly. The light status is also published via MQTT.

---

## Table of Contents

1. [Software Requirements](#software-requirements)
2. [Configuration](#configuration)
3. [Running the Script](#running-the-script)
4. [MQTT Topics](#mqtt-topics)
5. [Code Explanation](#code-explanation)
6. [Troubleshooting](#troubleshooting)
7. [References](#references)

---

## Software Requirements

- **Python 3.x**
- Required Python Libraries:
  - `paho-mqtt`: For MQTT messaging.
  - `os`: For environment variable management.

Install the required library using the following command:

```bash
pip3 install paho-mqtt
```

---

## Configuration

1. Set the MQTT broker IP as an environment variable. Add the following line to your `.bashrc` or `.profile` file:
    ```bash
    export IP="your-mqtt-broker-ip"
    ```
    Then, refresh the environment variables:
    ```bash
    source ~/.bashrc
    ```

---

## Running the Script

Run the script using:
```bash
python3 control_light.py
```

---

## MQTT Topics

The following MQTT topics are used:

| Topic                      | Description                               |
| ---------------------------| ------------------------------------------|
| `lightSensor`              | Receives the light sensor value            |
| `threshold`                | Receives the potentiometer value           |
| `LightStatus`              | Controls and receives the light status     |
| `Status/RaspberryPiC`      | Online/Offline status of the Raspberry Pi  |

---

## Code Explanation

1. **MQTT Callbacks:**
   - `on_connect`: Subscribes to `lightSensor`, `threshold`, and `LightStatus` topics upon connection.
   - `on_disconnect`: Publishes an "offline" status.
   - `on_message`: Updates `pot_value`, `ldr_value`, and `decision` variables with received data.
     - Compares the LDR and potentiometer values.
     - If the LDR value is greater than or equal to the potentiometer value, the light is turned off by publishing `TurnOff` to `LightStatus`.
     - If the LDR value is less than the potentiometer value, the light is turned on by publishing `TurnOn` to `LightStatus`.

2. **Decision Logic:**
    ```python
    if ldr_value >= pot_value and decision != "TurnOff":
        client.publish("LightStatus", "TurnOff", qos=2, retain=True)
    elif ldr_value < pot_value and decision != "TurnOn":
        client.publish("LightStatus", "TurnOn", qos=2, retain=True)
    ```

3. **Graceful Exit:**
    Handles disconnection by publishing an "offline" status.

---

## Troubleshooting

1. **MQTT Connection Issues:**
   - Verify the MQTT broker IP address is correctly set using:
     ```bash
     echo $IP
     ```

2. **No Light Status Change:**
   - Confirm the `lightSensor` and `threshold` topics are receiving the correct values.
   - Verify that the `LightStatus` topic is being published to.

---

## References

- [Paho MQTT Documentation](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)

---

