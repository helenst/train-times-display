from stations import haslemere as station

STATION = station.CODE

DIRECTIONS = station.DIRECTIONS

STATION_CODES = station.STATION_CODES


SERIAL_PORT = '/dev/ttyACM0'

import display
# Arduino
# DISPLAY = display.SerialDisplay

# Raspberry pi, using Adafruit char LCD lib
DISPLAY = display.GpioDisplay

# Enable this if testing without external device -
# output to console
#DISPLAY = display.DebugDisplay

import formats
FORMATTER = formats.SixteenByTwo
