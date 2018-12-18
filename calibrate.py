#!/usr/bin/python

import os
import busio
import digitalio
import board
import sys
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep, strftime, time

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

channel = AnalogIn(mcp, MCP.P0)
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
      channel = AnalogIn(mcp, MCP.P0)
      # set the max value to the biggest analog read value
      if channel.value > maxValue:
        maxValue = channel.value
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
