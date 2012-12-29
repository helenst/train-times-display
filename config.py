from stations import haslemere as station

STATION = station.CODE

DIRECTIONS = station.DIRECTIONS

STATION_CODES = station.STATION_CODES


SERIAL_PORT = '/dev/ttyACM0'

import display
DISPLAY = display.SerialDisplay

# Enable this if testing without external device -
# output to console
#DISPLAY = display.DummyDisplay

import formats
FORMATTER = formats.SixteenByTwo
