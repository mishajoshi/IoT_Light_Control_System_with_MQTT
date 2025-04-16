
# MQTT Message Logger for Raspberry Pi

This script logs incoming MQTT messages and tracks the state changes of an LED (LED1). It records timestamps for LED1 ON/OFF events in a separate file.

---

## Table of Contents

1. [Software Requirements](#software-requirements)
2. [Configuration](#configuration)
3. [Running the Script](#running-the-script)
4. [MQTT Topics](#mqtt-topics)
5. [Code Explanation](#code-explanation)
6. [Log Files](#log-files)
7. [Troubleshooting](#troubleshooting)
8. [References](#references)

---

## Software Requirements

- **Python 3.x**
- Required Python Libraries:
  - `paho-mqtt`: For MQTT communication.
  - `os`: For environment variable access.
  - `datetime`: For timestamp logging.

Install the required libraries using:

```bash
pip3 install paho-mqtt
```

---

## Configuration

1. Set the MQTT broker IP as an environment variable by adding this line to `.bashrc` or `.profile`:
    ```bash
    export IP="your-mqtt-broker-ip"
    ```
    Then, refresh the variables:
    ```bash
    source ~/.bashrc
    ```


---

## Running the Script

Run the script using:

```bash
python3 Laptop_#2.py
```

To stop execution, press `Ctrl+C`.

---

## MQTT Topics

The following topics are logged:

| Topic                      | Description                                   |
|----------------------------|-----------------------------------------------|
| `lightSensor`              | Light sensor readings                         |
| `threshold`                | Potentiometer threshold values                |
| `LightStatus`              | LED1 control messages                         |
| `Status/RaspberryPiA`      | Status updates from `RaspberryPiA`            |
| `Status/RaspberryPiC`      | Status updates from `RaspberryPiC`            |

---

## Code Explanation

1. **Logging Messages:**
    - All incoming MQTT messages are logged with timestamps in `MQTT_log.txt`.

2. **Tracking LED1 State:**
    - Changes in `LightStatus` are monitored.
    - When `LightStatus` is `"TurnOn"`, the timestamp is recorded in `led1_timestamps.txt`.
    - When `LightStatus` is `"TurnOff"`, the timestamp is also recorded.

3. **MQTT Callbacks:**
    - `on_connect`: Connects to the broker and subscribes to topics.
    - `on_message`: Logs received messages and tracks `LightStatus` changes.

4. **Graceful Exit:**
    - The script can be stopped with `Ctrl+C`, ensuring proper cleanup.

---

## Log Files

- **`MQTT_log.txt`**: Stores all MQTT messages with timestamps.
- **`led1_timestamps.txt`**: Stores only LED1 ON/OFF timestamps.

Example log entry in `MQTT_log.txt`:
```
[2025-02-18 14:30:25] LightStatus: TurnOn
```

Example log entry in `led1_timestamps.txt`:
```
[2025-02-18 14:30:25] LED1 ON
```

---

## Troubleshooting

1. **No MQTT Messages Logged:**
   - Ensure the broker IP is correctly set using:
     ```bash
     echo $IP
     ```

2. **Timestamps Not Recorded:**
   - Make sure messages are being published to `LightStatus`.

3. **Permission Issues:**
   - Ensure the script has write permissions for log files.

---

## References

- [Paho MQTT Documentation](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [Mosquitto MQTT Broker](https://mosquitto.org/)

---
