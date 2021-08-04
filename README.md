# Python-CMG

## Description

A program that automates the quality control for temperature and humidity sensors.
Takes plaintext log file of sensor data in sensor.log.
First line of the log are the reference temperatures and relative humidity.
The thermometer and humidity are listed with the sensor dates and readings.

## Technologies Used

Docker:
Python 3.8
Requirements:
NumPy - NumPy is the fundamental package for scientific computing in Python
Log file:
sensor.log
kubernetes deployment.yaml

## Setup

Docker
docker run --rm brian997/python-cmg:v2
Local
python app/main.py sensor.log

kubectl port-forward service/cmg-sensor-service 8000:80
