# Smart Parking IoT Project

## Introduction
Developed by Ali Haider & Giacomo Pedemonte, this Smart Parking IoT project utilizes cutting-edge technologies to optimize parking management. The project seamlessly integrates plate recognition, occupancy monitoring, and environmental tracking for efficient parking solutions.

## Table of Contents
- [Smart Parking IoT Project](#smart-parking-iot-project)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Smart Parking](#smart-parking)
  - [Simulation with ESP32](#simulation-with-esp32)
  - [Storing Time-Series Data (InfluxDB)](#storing-time-series-data-influxdb)
    - [InfluxDB - How it Works](#influxdb---how-it-works)
    - [InfluxDB - Data Collection](#influxdb---data-collection)
    - [InfluxDB - Data Exploration](#influxdb---data-exploration)
  - [Data Collection with Telegraf](#data-collection-with-telegraf)
  - [Visualization \& Alerting using Grafana](#visualization--alerting-using-grafana)
  - [Plate Recognition](#plate-recognition)
  - [Usage of WOKWI Simulator with PlatformIO](#usage-of-wokwi-simulator-with-platformio)
  - [Conclusion](#conclusion)

## Smart Parking
This system monitors entrances, exits, plate recognition, and parking occupancy/environment in real-time. Utilizes IoT devices for seamless integration.

## Simulation with ESP32
Simulation carried out using ESP32 microcontroller, providing a scalable, easy-to-use, and high-performance solution. Implemented with WOKWI for realistic testing.

## Storing Time-Series Data (InfluxDB)
InfluxDB, a high-performance Time Series Database, efficiently handles millions of data points per second. Ideal for DevOps monitoring, IoT applications, and real-time analytics. Organizes data into Buckets and Measurements for efficient storage and retrieval.

### InfluxDB - How it Works
- **Buckets:** Represent databases where measurements are stored.
- **Measurement:** Represents the data being measured, akin to a table.
- **Line Protocol:** InfluxDB stores data in Buckets using Line Protocol (LP) for time series representation.

### InfluxDB - Data Collection
InfluxDB provides tutorials for different programming languages. Run Telegraf as an MQTT consumer for seamless data ingestion.

### InfluxDB - Data Exploration
Explore data programmatically using InfluxDB Python client or interactively using InfluxDB UI. Query data, obtain results, and visualize insights.

## Data Collection with Telegraf
Telegraf, a plugin-driven server agent, collects, processes, aggregates, and writes metrics. Efficiently monitors various system parameters and IoT devices.

## Visualization & Alerting using Grafana
Grafana, a powerful visualization tool, integrates seamlessly with InfluxDB and Telegraf. Define contact points, set alert rules, and receive notifications via email or Telegram when conditions are met.

## Plate Recognition
Utilizes AI-based plate recognition that analyzes simulated pictures, monitoring vehicles inside the parking area.

## Usage of WOKWI Simulator with PlatformIO
Follow the instructions in the [WOKWI documentation](https://docs.wokwi.com/vscode/getting-started) to set up the WOKWI Simulator in your VS Code Workspace using PlatformIO. This integration provides an efficient way to simulate and test your ESP32-based Smart Parking IoT project.

## Conclusion
This Smart Parking IoT project leverages innovative technologies to revolutionize parking management. Seamlessly integrating plate recognition, occupancy monitoring, and environmental tracking, it offers a comprehensive solution for modern parking challenges. 

*Have a smooth parking experience!*
