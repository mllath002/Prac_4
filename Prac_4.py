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
SPICS = 8

reset_button = 17 # switch resets timer and cleans console 
freq_button = 26 # switch to change frequency
stop_button = 23 # switch off or on monitoring. Display when off.

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
GPIO.setup(switch_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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


freq_1 = 1/0.5 
freq_2 = 1/1.0 
freq_3 = 1/2.0

#global variable ?????
values = [0]*8

while True:
for i in range(8):
values[i] = mcp.read_adc(i)
 # delay for a half second
 time.sleep(0.5)
print values


# Open SPI bus
spi = spidev.SpiDev() # create spi object
spi.open(0,0)
# RPI has one bus (#0) and two devices (#0 & #1)
# function to read ADC data from a channel

# Define sensor channels
channel = 0
# Define delay between readings
delay = .5

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
def callback_freq(channel):
# change frequency of monitoring
# loop between 500ms, 1s, 2s 
def callback_stop(channel):
# stop or start monitoring sensors
# timer not affected but this functionality
# then display first five readings when stop switch pressed 


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
              





try:
GPIO.wait_for_edge(switch_3, GPIO.RISING)
except KeyboardInterrupt:
GPIO.cleanup() # clean up GPIO on CTRL+C exit
GPIO.cleanup() # clean up GPIO on normal exit


