#!/usr/bin/env python3
import os
from flask import Flask, request
from numpy import std


allData = []  
sensorReadings = {} 
cleanData = {}
fileError = []

uploadFolder = './upload'

app = Flask(__name__)
app.config['uploadFolder'] = uploadFolder

# flask server to post the sensor.log file
@app.route('/', methods=['GET', 'POST'])
def upload_file():
      if request.method == 'POST':
            if 'file1' not in request.files:
                  return 'there is no file1 in form!'
            file1 = request.files['file1']
            path = os.path.join(app.config['uploadFolder'], file1.filename)
            file1.save(path)
            file = 'upload/{0}'.format(file1.filename)
            processFile(file)
            return 'Processing: {0} ... Output: {1}{2}'.format(file1.filename, cleanData, fileError)
            
      return '''
      <h1>Upload new File</h1>
      <form method="post" enctype="multipart/form-data">
            <input type="file" name="file1">
            <input type="submit">
      </form>
      '''

# processing sensor file
def processFile(path):   
      
      # basic check if sensor.log file is being uploaded
      if path != "upload/sensor.log":
            errorMessage = "Wrong file type"
            fileError.append(errorMessage)
            os.remove(path)
            return fileError
      else:
            # inputs sensor.log file splits plaintext to string
            for line in open(path):
                  allData.append(line.split())
                  referenceTemp = float(allData[0][1])
                  referenceHumidity = float(allData[0][2])
                  
      # loop to create dictionary sensor key and sensor data as values
      for data in (allData):
            if data[0] == "reference":
                  # skips over the first line of log with reference data
                  continue
            elif data[0] == 'thermometer' or data[0] == 'humidity':
                  # sets list for the and key for sensor
                  sensorReadings[data[1]] = []
                  lastKey = data[1]      
            else: 
                  # values from sensor and appends to sensorReadins 
                  sensorData = float(data[1])
                  sensorReadings[lastKey].append(sensorData)

      # gets sensor values to determine status of sensors based on average and standard deviation 
      for sensor, values in sensorReadings.items():
            average = sum(values)/len(values)
            if 'temp' in sensor:
                  standardDeviation = std(values)
                  if average <= referenceTemp + 0.5 or average >= referenceTemp - 0.5:
                        if standardDeviation < 3:
                              sensorStatus = "ultra precise"
                        elif standardDeviation < 5:
                              sensorStatus = "very precise"
                        else:
                              sensorStatus = "precise"
            elif 'hum' in sensor:
                  if average > referenceHumidity + 1 or average < referenceHumidity - 1:
                        sensorStatus = "discard"
                  else:
                        sensorStatus = "keep"  
            # creates final output of clean data for the sensor status                
            cleanData[sensor] = sensorStatus
      os.remove(path)
            
      print(cleanData) 

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0")