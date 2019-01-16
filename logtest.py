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
import Adafruit_DHT as dht
import requests
import busio
import digitalio
import board
import sys
from math import sqrt
import Adafruit_MCP3008
from time import sleep, strftime, time
from csv import writer
import random

# Sensor ID
sensor_id = 'kl07'

# Software SPI configuration for MCP3008:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Header for csv file log
header = ['timestamp', 'voltage', 'temperature', 'humidity']


# Directory path of the log
directory = os.path.dirname(os.path.realpath(__file__)) + '/log/'

# Define DHT Type and PIN for temperature and humidity sensor
DHT_number = dht.DHT22
DHT_input_pin = 4

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

# Function for writing the current reading of all the sensor
# for displaying to web with interval of 5 sec
def currentWrite(filename, voltage, temperature, humidity):
  with open(filename, 'w') as now:
    now.write(str(voltage) + '\n')
    now.write(str(temperature) + '\n')
    now.write(str(humidity) + '\n')

# Function get analog reading from MCP3008
# Get the max value then sampling and
# do polynomial regression with spontaneous calculation

# Function to upload to ISP Dashboard
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
  # Define the interval of updating the file (in second)
  interval = 300 # 5 minutes interval
  # Define the url of api upload
  url = "http://122.248.39.155:5000/api/v1/upload"
  # Define the initial timer
  currentTimer = time()
  sensorTimer = time()
  # Define max value counter
  maxValue = 0
  # initial timer
  t = time()
  # initial total voltage
  vtotal = 0
  try:
    # Begin the infinite loop
    while True:
      # set the current timer
      timer = time()
      # set the date when the data is collected
      date = strftime("%Y-%m-%d")
      # set the filename of the csv file per day
      filename = directory + sensor_id + '-' + date + '.csv'
      filename_current = directory + '-now.txt'
      humidity, temperature = dht.read_retry(DHT_number, DHT_input_pin)
      temperature = round(temperature,1)
      humidity = round(humidity,1)
      #temperature = random.randint(20,30)
      #humidity = random.randint(60,70)
      #vtotal = random.randint(200,230)
      v2 = 0
      vsquare = 0
      for i in range(100):
        channel = mcp.read_adc(0)
        v = -0.0008 * channel * channel + 2.8891 * channel - 1233.5
        v2 = v*v
        vsquare = vsquare + v2
      vtotal = sqrt(vsquare/100) + 50
      if vtotal < 100.00:
         vtotal = 0.00
      vtotal = round(vtotal,2)
      #data = collectData(vtotal, temperature, humidity)
      if timer - t >= 5:
        currentWrite(filename_current, vtotal, temperature, humidity)
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

