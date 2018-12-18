from time import sleep, strftime, time
import Adafruit_MCP3008

# Software SPI configuration for MCP3008:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def main():
  vpp = 0
  maxValues = 0
  minValues = 1023
  t = time()
  tv = time()
  vtotal = 0
  try:
    while True:
      t1 = time()
      if t1 - t  >= 1:
        t = time()
        #print(maxValues)
        #print(minValues)
        #print("analog= {}".format(maxValues))
        print("AC Voltage RMS= {}".format(vtotal))
        maxValues = 0
      reading = mcp.read_adc(0)
      if reading > maxValues:
        maxValues = reading
      for i in range(100):
        vrms = -0.0008 * maxValues * maxValues + 2.8891 * maxValues - 1233.5
        vtotal += vrms
      vtotal = vtotal/100

  except KeyboardInterrupt:
    print("Program Stopped")

if __name__ == "__main__":
  print("Starting Program")
  print("----------------")
  print("Logging")
  main()


