# Functions to be called by main.py

# Import necessary modules
import serial
import time


#########################################################################################################

# Open Serial Communications with Arduino

def Open_Comms():
    arduino = serial.Serial(port='com4',baudrate=9600,timeout=.1)
    time.sleep(2)
    return arduino

#########################################################################################################


