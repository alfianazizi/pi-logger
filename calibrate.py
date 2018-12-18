#!/usr/bin/python

import os
import busio
import digitalio
import board
import sys
import Adafruit_MCP3008
from time import sleep, strftime, time

# Software SPI configuration for MCP3008:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

t = time()
try:
  while True:
    vpp = 0
    # Define max value counter
    maxValue = 0
    # initial timer
    t = time()
    # initial total voltage
    vtotal = 0
    try:
      # initial timer for interval counter
      t1 = time()
      # reset the max value with interval of 1 sec
      if t1 - t >= 1:
        # reset the counter
        t = time()
        print(maxValue)
        maxValue = 0
      # get analog read from mcp3008
      channel = mcp.read_adc(0)
      # set the max value to the biggest analog read value
      if channel > maxValue:
        maxValue = channel
      # loop to get the average
      # for i in range(20):
      #   # Polynomial regression
      #   vrms = -0.0004 * maxValue * maxValue + 2.3738 * maxValue - 1030.6
      #   vtotal += vrms
      # vtotal = vtotal/20
    except KeyboardInterrupt:
      print("Calibration Stopped")
      sys.exit(0)
except KeyboardInterrupt:
  print("Calibration Stopped")
  sys.exit(0)
