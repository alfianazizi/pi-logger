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
import Adafruit_MCP3008
from time import sleep, strftime, time
from csv import writer

# Sensor ID
sensor_id = 'klogger01'

# Software SPI configuration for MCP3008:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Header for csv file log
header = ['Timestamp', 'AC Voltage', 'Temperature', 'Humidity']

# Directory path of the log
directory = os.path.dirname(os.path.realpath(__file__)) + '/log/'

# Define DHT Type and PIN for temperature and humidity sensor
DHT_number = dht.DHT11
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
  with open(filename, 'a') as log:
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
def getVoltage(sensorpin):
  # Initiate voltage peak
  vpp = 0
  # Define max value counter
  maxValue = 0
  # initial timer
  t = time()
  # initial total voltage
  vtotal = 0
  # initial timer for interval counter
  t1 = time()
  # reset the max value with interval of 1 sec
  if t1 - t >= 1:
    # reset the counter
    t = time()
    maxValue = 0
  # get analog read from mcp3008
  channel = mcp.read_adc(0)
  # set the max value to the biggest analog read value
  if channel > maxValue:
    maxValue = channel
  # loop to get the average
  for i in range(20):
    # Polynomial regression
    vrms = -0.0004 * maxValue * maxValue + 2.3738 * maxValue - 1030.6
    vtotal += vrms
  vtotal = vtotal/20
  return vtotal

# Function to upload to ISP Dashboard
def upload(url, file):
  try:
    r = requests.post(url, files=file)
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
  try:
    # Begin the infinite loop
    while True:
      # set the current timer
      timer = time()
      # set the date when the data is collected
      date = strftime("%Y-%m")
      # set the filename of the csv file per day
      filename = directory + sensor_id + '-' + date + '.csv'
      filename_now = directory + sensor_id + '-now.txt'
      humidity, temperature = dht.read_retry(DHT_number, DHT_input_pin)
      # Get the voltage
      ac_voltage = getVoltage(sensorVolt)
      # write the sensor
      if timer - currentTimer >= interval:
        data = collectData(ac_voltage, temperature, humidity)
        writeData(data)
        upload(url, files)
        currentTimer = time()
      #write the current reading
      if timer - sensorTimer >= 5:
        currentWrite(filename_now, ac_voltage, temperature, humidity)
        print("Temperature: {}, Humidity: {}". format(temperature,humidity))
        try:
          files = {'file': open(filename, 'rb')}
        except:
          pass
        sensorTimer = time()
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
