from stations import haslemere as station

STATION = station.CODE

DIRECTIONS = station.DIRECTIONS

STATION_CODES = station.STATION_CODES

# This many minutes or longer counts as a severe delay
SEVERE_DELAY_THRESHOLD = 5

SERIAL_PORT = '/dev/ttyACM0'

import display
# Arduino
# DISPLAY = display.SerialDisplay

# Raspberry pi, using Adafruit char LCD lib
DISPLAY = display.RgbGpioDisplay

# Gpio pins used for backlight control
# (We don't actually use blue so haven't wired it up to anything)
BACKLIGHT_GREEN = 4
BACKLIGHT_BLUE = 0
BACKLIGHT_RED = 18

# LED type used for backlight
# common anode (e.g. the Adafruit ones) - set low to switch on (0, 1)
# common cathode LEDs (many others) - set high to switch on (1, 0)
BACKLIGHT_ON, BACKLIGHT_OFF = (0, 1)

# Pi revision (quick check: does it have two mounting holes? If so, it's revision 2)
# Affects pin mappings in char lcd code
PI_REVISION = 2

# Enable this if testing without external device -
# output to console
#DISPLAY = display.DebugDisplay

import formats
FORMATTER = formats.SixteenByTwo

# Range of hours in which we should not bother fetching times
# it saves on pointless requests and also prevents this thing
# lighting up at 4am when the first trains go onto the board!.
# e.g. range(1,5) means between 1am and 4:49am
QUIET_HOURS = range(1,6)
