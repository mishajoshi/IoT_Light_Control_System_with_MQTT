
# Raspberry Pi MQTT Sensor Monitoring

This project uses a Raspberry Pi with an ADS7830 ADC to read values from an LDR (Light Dependent Resistor) and a potentiometer. The data is published via MQTT, allowing remote monitoring of light and threshold values. It also listens for updates to these values via MQTT and adjusts accordingly.

---

## Table of Contents

1. [Hardware Requirements](#hardware-requirements)
2. [Software Requirements](#software-requirements)
3. [Circuit Diagram](#circuit-diagram)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the Script](#running-the-script)
7. [MQTT Topics](#mqtt-topics)
8. [Code Explanation](#code-explanation)
9. [Troubleshooting](#troubleshooting)
10. [References](#references)

---

## Hardware Requirements

1. Raspberry Pi (with I2C support)
2. ADS7830 ADC Module
3. LDR (Light Dependent Resistor)
4. Potentiometer
5. Jumper Wires

---

## Software Requirements

- **Python 3.x**
- Required Python Libraries:
  - `smbus`: For I2C communication.
  - `paho-mqtt`: For MQTT messaging.
  - `os`: For environment variable management.
  - `time`: For sleep intervals.

Install the necessary libraries using the following commands:

```bash
sudo apt update
sudo apt install python3-smbus python3-pip
pip3 install paho-mqtt
```

---

## Circuit Diagram

Connect the components as follows:

| Component       | Raspberry Pi GPIO | ADS7830 Channel |
| --------------- | ----------------- | --------------- |
| LDR             | A0                | Channel 6       |
| Potentiometer   | A1                | Channel 7       |
| ADS7830 VCC     | 3.3V              |                 |
| ADS7830 GND     | GND               |                 |
| ADS7830 SDA     | GPIO 2 (SDA1)     |                 |
| ADS7830 SCL     | GPIO 3 (SCL1)     |                 |

**Note:** Make sure the I2C interface is enabled on your Raspberry Pi. You can enable it using:

```bash
sudo raspi-config
```
Navigate to **Interfacing Options** and enable **I2C**.

---

## Installation

1. Clone the repository or copy the script to your Raspberry Pi:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Install the required dependencies:
    ```bash
    pip3 install paho-mqtt
    ```

3. Ensure the I2C module is loaded:
    ```bash
    ls /dev/i2c*
    ```

4. Check if the ADS7830 is detected:
    ```bash
    sudo i2cdetect -y 1
    ```
   The device should be listed at address `0x48`.

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
python3 read_light_pot.py
```

---

## MQTT Topics

The following MQTT topics are used:

| Topic                      | Description                               |
| ---------------------------| ------------------------------------------|
| `lightSensor`              | Publishes the light sensor value           |
| `threshold`                | Publishes the potentiometer value          |
| `Status/RaspberryPiA`      | Online/Offline status of the Raspberry Pi  |

---

## Code Explanation

1. **I2C Initialization:**
    ```python
    bus = smbus.SMBus(1)
    ADS7830_ADDRESS = 0x48
    ```

2. **MQTT Callbacks:**
   - `on_connect`: Subscribes to `lightSensor` and `threshold` topics upon connection.
   - `on_disconnect`: Publishes an "offline" status.
   - `on_message`: Updates `prev_light` and `prev_pot` variables with received data.

3. **Reading ADC Values:**
    ```python
    ldr_value = bus.read_byte_data(ADS7830_ADDRESS, translate_address(6))/255
    pot_value = bus.read_byte_data(ADS7830_ADDRESS, translate_address(7))/255
    ```

4. **Publishing Data:**
    ```python
    client.publish('lightSensor', payload=ldr_value, qos=2, retain=True)
    client.publish('threshold', payload=pot_value, qos=2, retain=True)
    ```

5. **Graceful Exit:**
    Handles `KeyboardInterrupt` to stop the loop and disconnect MQTT.

---

## Troubleshooting

1. **I2C Errors:**
   - Ensure I2C is enabled using `sudo raspi-config`.
   - Confirm the device is detected with:
     ```bash
     sudo i2cdetect -y 1
     ```

2. **MQTT Connection Issues:**
   - Verify the MQTT broker IP address is correctly set using:
     ```bash
     echo $IP
     ```

3. **No Sensor Data:**
   - Check wiring connections.
   - Verify the ADS7830 address with `i2cdetect`.

---

## References

- [Paho MQTT Documentation](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [Raspberry Pi I2C Setup](https://www.raspberrypi.org/documentation/configuration/)
- [ADS7830 Datasheet](https://www.ti.com/lit/ds/symlink/ads7830.pdf)

---

