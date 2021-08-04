# Python-CMG

## Description

Python-CMG is a program that automates the quality control for temperature and humidity sensors.
This uses a Flask server in a docker container then uses kubernetes to connect to your local network.
This app takes a plaintext log file of sensor data in a sensor.log file.
This sensor.log file can be found under the log/ directory in this repo.

## Assumptions

The log file is assumed to be sensor.log without any formatting.
Unknowns are file size, multiple files, sensor scaling, text formatting, error handling and final output.
The first line of the log set the reference temperatures and relative humidity.
The thermometer and humidity sensors are listed with the sensor dates and readings.

## Technologies Used

Docker:
Python 3.8
Requirements found in the requirements.txt:
NumPy - NumPy is the fundamental package for scientific computing in Python
Flask - Simple server used to upload the file.

Log file:
sensor.log
Docker Hub:
DIGEST:sha256:394a4403e469c962f36ab439ba3f33e1ea0c59cb46a5023412b568142a1b7fe8
Kubernetes
app.yaml

## Improvements

File handling
Dynamically add new sensors
Error reporting
Improved output
Smaller Docker Image
Improved UI

## Setup

Docker
docker pull brian997/python-cmg
docker run --rm brian997/python-cmg:v4
kubectl port-forward service/cmg-sensor-service 8000:80

In main.py, flask is started a simple server on localhost:8000 and a basic html form to upload is presented.
On submit, the file is passed to process the sensor data file.
The evaluation criteria are:

1. For a thermometer, it is branded “ultra precise” if the mean of the readings is within 0.5 degrees of the known temperature, and the standard deviation is less than 3. It is branded “very precise” if the mean is within 0.5 degrees of the room, and the standard deviation is under 5. Otherwise, it’s sold as “precise”.
2. For a humidity sensor, it must be discarded unless it is within 1 humidity percent of the reference value for all readings. (All humidity sensor readings are a decimal value representing percent moisture saturation.)
