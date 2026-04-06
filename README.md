# IO-Link Dashboard System

## Overview
This project is an industrial IoT diploma project for processing and visualizing sensor data.

The goal is to build a structured system that connects IO-Link sensor data with a modern web dashboard. The project focuses on real-time communication, backend architecture, sensor metadata processing, and modular system design.

## Architecture

```text
IO-Link Sensor
   ↓
IO-Link Master
   ↓
MQTT Broker (Mosquitto)
   ↓
Backend (NestJS)
   ↓
Frontend (Vue.js)

Additional service:
Python Service → parses IODD files and extracts sensor metadata
````

## Technologies

* Backend: NestJS (Node.js)
* Frontend: Vue.js
* Data Processing: Python
* IODD Parsing: iodd-parser
* Communication: MQTT (Mosquitto)
* Environment: Linux (Debian)

## Features

* Real-time sensor data communication via MQTT
* Structured backend API with NestJS
* Python service for IODD file parsing
* Extraction and processing of sensor metadata
* Modular project structure
* Web-based dashboard for sensor visualization

## Project Structure

```text
backend/          # NestJS API
frontend/         # Vue.js dashboard
python-service/   # Python service for IODD parsing
docs/             # project documentation
```

## Example Workflow

1. The sensor sends process data
2. The IO-Link Master forwards the data
3. MQTT distributes the messages
4. The NestJS backend receives and processes the data
5. The frontend displays the sensor values
6. The Python service provides parsed IODD metadata

## Current Status

This project is currently a work in progress.

Implemented so far:

* MQTT communication
* Basic backend API structure
* Python-based IODD parsing
* Basic frontend dashboard

Planned next steps:

* WebSocket integration
* Database integration (InfluxDB or SQL)
* Improved UI structure
* Alert and monitoring features

## Why this project?

This project demonstrates:

* industrial communication basics
* IO-Link related system integration
* MQTT-based real-time data flow
* backend and frontend interaction
* Python-based metadata processing
* modular full-stack architecture

## Author

Viktor Borosnyai


