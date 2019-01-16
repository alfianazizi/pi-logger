#!/usr/bin/python

#             DATA LOGGER - KIREI
# This is data logger code tested for raspberry pi 3 to record AC voltage, temperature, and humidity
#          It is currently being worked on

# Pin information
#
#
#
#

import os
import requests
import sys
from time import sleep, strftime, time
from csv import writer

# Sensor ID
sensor_id = 'kl07'

# Header for csv file log
header = ['timestamp', 'voltage', 'temperature', 'humidity']

# Directory path of the log
directory = os.path.dirname(os.path.realpath(__file__)) + '/log/'

# Collect the array template for writing to csv file
def collectData(voltage, temperature, humidity):
  data = []
  # Append the timestamp to the first element of array
  data.append(strftime("%Y-%m-%d %H:%M:%S"))
  data.append(voltage)
  data.append(temperature)
  data.append(humidity)
  return data

# Function to write to csv file
def writeData(filename, data):
  # Open the file csv as log
  with open(filename, 'a', encoding='utf-8') as log:
    # Check if the file is exist
    file_is_empty = os.stat(filename).st_size == 0
    temp_writer = writer(log, lineterminator='\n')
    # If the file not exist, print the header
    if file_is_empty:
      temp_writer.writerow(header)
    # else print don't print the header
    temp_writer.writerow(data)

def readData(filename):
  with open(filename) as f:
    lines = f.readlines()
  return lines

def upload(url, files):
  try:
    file = {'file': open(files, 'rb')}
    r = requests.post(url, files=file)
    print(r.text)
  except requests.exceptions.RequestException as e:
    print(e)
    pass

# the main function here
def main():
  url = "http://122.248.39.155:5000/api/v1/upload"
  # Define the initial timer
  t = time()

  try:
    # Begin the infinite loop
    while True:
      timer = time()
      date = strftime("%Y-%m-%d")
      filename = directory + sensor_id + '-' + date + '.csv'
      filename_current = directory + 'sensor-now.txt'
      file = readData(filename_current)
      data = collectData(file[0], file[1], file[2])
      if timer - t >= 60:
        writeData(filename, data)
        print("AC Voltage: {}, Temperature: {}, Humidity: {}". format(vtotal,temperature,humidity))
        t = time()
  # except cancelled by user
  except KeyboardInterrupt:
    print("Program Stopped by user")
    sys.exit(0)

# Main Program
if __name__ == "__main__":
  print("Starting Program")
  print("----------------")
  print("--Logging Data--")
  print("----------------")
  main()

