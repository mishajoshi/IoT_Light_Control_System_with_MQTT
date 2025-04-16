
# Raspberry Pi LED Control via MQTT

This project uses a Raspberry Pi to control three LEDs based on MQTT messages. The LEDs represent the status of light control and the online/offline status of two other Raspberry Pis.

---

## Table of Contents

1. [Software Requirements](#software-requirements)
2. [Hardware Setup](#hardware-setup)
3. [Configuration](#configuration)
4. [Running the Script](#running-the-script)
5. [MQTT Topics](#mqtt-topics)
6. [Code Explanation](#code-explanation)
7. [Troubleshooting](#troubleshooting)
8. [References](#references)

---

## Software Requirements

- **Python 3.x**
- Required Python Libraries:
  - `paho-mqtt`: For MQTT messaging.
  - `RPi.GPIO`: For controlling the GPIO pins on the Raspberry Pi.
  - `os`: For environment variable management.

Install the required libraries using the following commands:

```bash
pip3 install paho-mqtt
sudo apt install python3-rpi.gpio
```

---

## Hardware Setup

Connect the LEDs as follows:
- **LED1**: GPIO 17 - Represents light control status.
- **LED2**: GPIO 27 - Represents the status of `RaspberryPiA`.
- **LED3**: GPIO 22 - Represents the status of `RaspberryPiC`.

Make sure to use appropriate resistors to protect the LEDs.

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
sudo python3 RPI_B.py
```

> **Note**: `sudo` is required because GPIO access on the Raspberry Pi requires root privileges.

---

## MQTT Topics

The following MQTT topics are used:

| Topic                      | Description                                    |
| ---------------------------| ------------------------------------------------|
| `LightStatus`              | Controls LED1 for light status                  |
| `Status/RaspberryPiA`      | Controls LED2 for `RaspberryPiA` status          |
| `Status/RaspberryPiC`      | Controls LED3 for `RaspberryPiC` status          |

---

## Code Explanation

1. **GPIO Setup:**
    - Configures GPIO pins 17, 27, and 22 for output to control the LEDs.
    - Initializes all LEDs to the OFF state.

2. **MQTT Callbacks:**
    - `on_connect`: Subscribes to relevant MQTT topics.
    - `on_message`: Handles messages for the following topics:
        - **LightStatus**: Controls LED1 for light on/off status.
        - **Status/RaspberryPiA**: Controls LED2 to indicate online/offline status.
        - **Status/RaspberryPiC**: Controls LED3 to indicate online/offline status and restores LED1 state if necessary.

3. **Handling Reconnection:**
    - Restores the state of LED1 based on the last known `LightStatus` value when `RaspberryPiC` reconnects.

4. **Graceful Exit:**
    - Handles disconnection and cleans up GPIO states when the script is stopped using `Ctrl+C`.

---

## Troubleshooting

1. **MQTT Connection Issues:**
   - Verify the MQTT broker IP address is correctly set using:
     ```bash
     echo $IP
     ```

2. **LEDs Not Working:**
   - Confirm the wiring connections and GPIO pins used.

3. **Incorrect LED Behavior:**
   - Make sure the correct MQTT messages are being published on the expected topics.

---

## References

- [Paho MQTT Documentation](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [RPi.GPIO Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)

---


