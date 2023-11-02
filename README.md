# Smart Parking IoT Project

## Introduction
Developed by [Ali Haider](https://github.com/AliHaider-codes/AliHaider-codes) & Giacomo Pedemonte, this Smart Parking IoT project utilizes cutting-edge technologies to optimize parking management. The project seamlessly integrates plate recognition, occupancy monitoring, and environmental tracking for efficient parking solutions.

## Table of Contents
- [Smart Parking IoT Project](#smart-parking-iot-project)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Smart Parking](#smart-parking)
  - [Requirements](#requirements)
    - [Usage of WOKWI Simulator with PlatformIO in VS](#usage-of-wokwi-simulator-with-platformio-in-vs)
  - [How SMART PARKING works?](#how-smart-parking-works)
    - [Simulation with ESP32](#simulation-with-esp32)
    - [Visualize and Interact with the Simulation](#visualize-and-interact-with-the-simulation)
    - [Storing Time-Series Data (InfluxDB)](#storing-time-series-data-influxdb)
      - [InfluxDB - How it Works](#influxdb---how-it-works)
      - [InfluxDB - Data Collection](#influxdb---data-collection)
      - [Data Collection with Telegraf](#data-collection-with-telegraf)
      - [InfluxDB - Data Exploration](#influxdb---data-exploration)
    - [Visualization \& Alerting using Grafana](#visualization--alerting-using-grafana)
    - [Plate Recognition](#plate-recognition)
  - [Conclusion](#conclusion)

## Smart Parking
This system monitors entrances, exits, plate recognition, and parking occupancy/environment in real-time. Utilizes IoT devices for seamless integration.

## Requirements
You will need to have correctly installed in Visual Studio PlatformIO extension to create the correct environment. The integration will be also with Wokwi for Visual Studio.

### Usage of WOKWI Simulator with PlatformIO in VS
Follow the instructions in the [WOKWI documentation](https://docs.wokwi.com/vscode/getting-started) to set up the WOKWI Simulator in your VS Code Workspace using [PlatformIO](https://platformio.org/install/ide?install=vscode).

This integration provides an efficient way to simulate and test your ESP32-based Smart Parking IoT project. All the information about the Board will be visible and setted inside the .pio folder. Use also the PIO interface to setup correctly the environment.

Now you will need to simply use PIO platform interface to build the workspace and check if all is working fine.

## How SMART PARKING works?

### Simulation with ESP32
Simulation carried out using ESP32 microcontroller, providing a scalable, easy-to-use, and high-performance solution. Implemented with WOKWI for realistic testing. 

### Visualize and Interact with the Simulation

After requiring the Wokwi license to use Wokwi free in VS, you will be able to start the simulation directly inside VS. Watch this simple [video](https://wokwi.github.io/video-assets/vscode/wokwi-vscode-1s.mp4) provided by Wokwi.

### Storing Time-Series Data (InfluxDB)
[InfluxDB](https://www.influxdata.com/), a high-performance Time Series Database, efficiently handles millions of data points per second. Ideal for DevOps monitoring, IoT applications, and real-time analytics. Organizes data into Buckets and Measurements for efficient storage and retrieval.

#### InfluxDB - How it Works
- **Buckets:** Represent databases where measurements are stored.
- **Measurement:** Represents the data being measured, akin to a table.
- **Line Protocol:** InfluxDB stores data in Buckets using Line Protocol (LP) for time series representation.

#### InfluxDB - Data Collection
InfluxDB provides tutorials for different programming languages. Run Telegraf as an MQTT consumer for seamless data ingestion.

#### Data Collection with Telegraf
[Telegraf](https://www.influxdata.com/time-series-platform/telegraf/), a plugin-driven server agent, collects, processes, aggregates, and writes metrics. Efficiently monitors various system parameters and IoT devices.

#### InfluxDB - Data Exploration
Explore data programmatically using InfluxDB Python client or interactively using InfluxDB UI. Query data, obtain results, and visualize insights.

### Visualization & Alerting using Grafana
[Grafana](https://grafana.com/), a powerful visualization tool, integrates seamlessly with InfluxDB and Telegraf. Define contact points, set alert rules, and receive notifications via email or Telegram when conditions are met.

### Plate Recognition
Utilizes AI-based plate recognition that analyzes simulated pictures, monitoring vehicles inside the parking area. Run the [PlateRecogntion.ipynb](https://github.com/PedemonteGiacomo/SmartParking/blob/main/PlateRecognition.ipynb) to see the results.

Plate recognition script is called whenever a car enter or leave the park to manage correctly the plate analysis.

Change the following with a picture of a car in the front or in the back:

```py
img = cv2.imread('license-plates/capture.jpg')
```

## Conclusion
This Smart Parking IoT project leverages innovative technologies to revolutionize parking management. Seamlessly integrating plate recognition, occupancy monitoring, and environmental tracking, it offers a comprehensive solution for modern parking challenges. 

*Have a smooth parking experience!*
