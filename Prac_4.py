# -*- coding: cp1252 -*-
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import spidev 
import time
import os
import sys

GPIO.setmode(GPIO.BCM) #pin numbering BCM

# pin definition
# for SPI pin 9-11
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10

reset_button = 17 # switch resets timer and cleans console 
freq_button = 26 # switch to change frequency
stop_button = 23 # switch off or on monitoring. Display when off.
disp_button = 6 # display the first five readings

# sensors channel 0-7 definition MCP3008
light_channel = 0
temp_channel = 1 
pot_channel = 2

# set outputs 
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
#set inputs
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(reset_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(freq_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(disp_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# when falling egde detected on the pin numbers
# the following functions will run
GPIO.add_event_detect(reset_button, GPIO.FALLING, callback=callback_reset,
bouncetime=200)
GPIO.add_event_detect(freq_button, GPIO.FALLING, callback=callback_freq,
bouncetime=200)
GPIO.add_event_detect(stop_button, GPIO.FALLING, callback=callback_stop,
bouncetime=200)

# Open SPI bus
spi = spidev.SpiDev() # create spi object
spi.open(0,0)

# Define delay between readings
delay = .5

# what this line does, i have no clue. 
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

# reset_button_pressed = True
# freq_button_pressed = True
# stop_button_pressed = True

# global variable ?????
# values = [0]*8

try:
while True:
# read light sensor data 
 sensor_data = GetData (light_channel)
 sensor_volt = ConvertVolts(sensor_data,2)
# read temp sensor data 
 sensor_data = GetData (temp_channel)
 sensor_volt = ConvertVolts(sensor_data,2)
# read pot sensor data 
 sensor_data = GetData (pot_channel)
 sensor_volt = ConvertVolts(sensor_data,2)
# Wait before repeating loop
 time.sleep(delay)
except KeyboardInterrupt:
 spi.close()



# FUNCTION DEFINITION: threaded callback
def callback_reset(channel):
# reset timer and clean console
 unused = os.system("clear') 
 global total 
 total = 0 
 print("Time\t\tTimer\tPot\tTemp\tLight")
 
   
def callback_freq(channel):
# change frequency of monitoring
# loop between 500ms, 1s, 2s 
 global delay
  if(delay==0.5):
    delay = 1
  elif(delay==1):
    delay = 2
  else: 
    delay = 0.5

def callback_stop(channel):
# stop or start monitoring sensors
# timer not affected but this functionality
# then display first five readings when stop switch pressed 
   global stop 
   global count 
   if(stop==False):
     stop = True
     count = 0 
   else: 
     stop = False

 def callback_display(channel): 
 # display first five readings after stop button pressed 
   global display
   print("*****************DISPLAY********************")
   print("Time\t\tTimer\tPot\tTemp\tLight")
   for i in range(5): 
      print(display[i])
   print("********************************************")                 
                    


# FUNCTION DEFINITION: get data from channels 
def GetData(0): # light_channel
 adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes
 data = ((adc[1]&3) << 8) + adc[2]
 return data
def GetData(1): # temp_channel
 adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes
 data = ((adc[1]&3) << 8) + adc[2]
 return data
def GetData(2): # pot_channel
 adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes
 data = ((adc[1]&3) << 8) + adc[2]
 return data

# FUNCTION DEFINITION: convert data to voltage 
def ConvertVolts(data,places): # places: number of decimal places needed
 volts = (data * 3.3) / float(1023)
 volts = round(volts,2) #round of to two decimal places
 return volts

# FUNCTION DEFINITION: convert data to temperature 
def ConvertTemp(data): 
 temp = ((data*330/float(1023))-50
 temp = round(temp,0) #round to zero decimal places 
 return temp #return temp in degrees 

# FUNCTION DEFINITION: convert data to percentage
def ConvertPercent(data): 
         # ????
              
# 'bouncetime=200' includes the bounce control
# ‘bouncetime=200’ sets 200 milliseconds during which second button press will be ignored.
# to remove: GPIO.remove_event_detect(port_number)



# try:
# GPIO.wait_for_edge(switch_3, GPIO.RISING)
# except KeyboardInterrupt:
# GPIO.cleanup() # clean up GPIO on CTRL+C exit
# GPIO.cleanup() # clean up GPIO on normal exit

