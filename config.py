from stations import haslemere as station

STATION = station.CODE

DIRECTIONS = station.DIRECTIONS

STATION_CODES = station.STATION_CODES


SERIAL_PORT = '/dev/ttyACM0'

import display
# Arduino
# DISPLAY = display.SerialDisplay

# Raspberry pi, using Adafruit char LCD lib
DISPLAY = display.RgbGpioDisplay

# Gpio pins used for backlight control
# No 'R' in the RGB for now.
# (a) I ran out of pins
# (b) I blew the red LED :(
BACKLIGHT_GREEN = 4
BACKLIGHT_BLUE = 18

# Enable this if testing without external device -
# output to console
#DISPLAY = display.DebugDisplay

import formats
FORMATTER = formats.SixteenByTwo
