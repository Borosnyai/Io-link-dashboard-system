# Io-link-dashboard-system

# IO-Link Dashboard System

## Overview
This project is an industrial IoT system for processing and visualizing sensor data.

It connects IO-Link sensors with a modern web dashboard and enables structured, real-time data handling.

---

## Architecture

IO-Link Sensor → IO-Link Master → MQTT → Backend (NestJS) → Frontend (Vue.js)

Additional component:
- Python Service → parses IODD files and extracts sensor metadata

---

## Technologies

- Backend: NestJS (Node.js)
- Frontend: Vue.js
- Data Processing: Python (iodd-parser)
- Communication: MQTT (Mosquitto)
- Environment: Linux (Debian)

---

## Features

- Real-time sensor data processing via MQTT
- Structured backend API (REST)
- IODD file parsing (Python service)
- Modular system architecture
- Web-based dashboard visualization

---

## Project Structure
backend/ # NestJS API
frontend/ # Vue.js Dashboard
python-service/ # IODD parsing service
docs/ # documentation


---

## Example Workflow

1. Sensor sends process data
2. IO-Link Master forwards data
3. MQTT broker distributes messages
4. Backend processes and structures data
5. Frontend displays sensor values

---

## Status

Work in progress (Diploma project)

Current progress:
- MQTT communication implemented
- Backend API structure ready
- Python IODD parsing working
- Frontend basic dashboard

Planned:
- WebSocket integration
- Database integration (InfluxDB / SQL)
- UI improvements
- Alert system

---

## Why this project?

This project demonstrates:
- understanding of industrial communication (IO-Link, MQTT)
- backend architecture design
- real-time data processing
- integration of multiple technologies

---

## Author

Viktor Borosnyai
