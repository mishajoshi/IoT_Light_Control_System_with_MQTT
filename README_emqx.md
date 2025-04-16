EMQX MQTT Broker Setup and Usage

Introduction

EMQX is a powerful and scalable open-source MQTT broker designed for IoT applications. This guide will help you install EMQX using Docker.

Installation

1. Install EMQX

For detailed installation instructions, visit: EMQX Installation Guide

2. Docker Installation

If you prefer to use Docker, follow these steps:

a) Get Docker Image

docker pull emqx/emqx:5.8.4

b) Start Docker Container

docker run -d --name emqx \
    -p 1883:1883 -p 8083:8083 -p 8084:8084 \
    -p 8883:8883 -p 18083:18083 emqx/emqx:5.8.4

Web Dashboard

EMQX provides a web-based dashboard to monitor MQTT activities.

Access the Dashboard

Open a browser and navigate to:

http://localhost:18083

(Default username: admin, password: public)
