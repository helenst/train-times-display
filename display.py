import config
import serial

from Adafruit_CharLCD import Adafruit_CharLCD
from RPi import GPIO

class DeviceTimeoutError(Exception):
    pass


class DebugDisplay:
    """Terminal display of train data and commands"""

    def __init__(self, *args):
        pass

    def write(self, string):
        print(string)

    def move_to(self, row, col):
        print("move to {}, {}".format(row, col))

    def clear(self):
        print("clear")

    def backlight(self, r, g, b):
        print("set backlight ({}, {}, {})".format(r,g,b))


class SerialDisplay:

    def __init__(self, rate=9600, cols=16, rows=2):
        self.port = serial.Serial(config.SERIAL_PORT, rate, timeout=10)
        self.wait_for_ready()
        self.cols = cols
        self.rows = rows

    # Serial connection resets arduino.
    # Wait for this to complete (send a zero) before pushing any data
    def wait_for_ready(self):
        data = self.port.read()
        if data and data[0] == 0:
            # Got the expected ready signal
            return
        else:
            raise DeviceTimeoutError('Timed out waiting for serial ready')

    def clear(self):
        self.port.write('c'.encode())

    def move_to(self, col, row):
        self.port.write(bytearray([ord('m'), col, row]))

    def write(self, string):
        self.port.write('w{0}\0'.format(string).encode())
        self.port.flush()

    def backlight(self, r, g, b):
        # not implemented
        pass


class GpioDisplay:

    def __init__(self, *_args):
        if config.PI_REVISION == 2:
            self.lcd = Adafruit_CharLCD(pins_db=[23, 17, 27, 22])
        else:
            self.lcd = Adafruit_CharLCD()
        self.lcd.begin(16,2)

    def clear(self):
        self.lcd.clear()

    def move_to(self, row, col):
        self.lcd.setCursor(row, col)

    def write(self, string):
        self.lcd.message(string)

    def backlight(self, r, g, b):
        # not implemented
        pass


class RgbGpioDisplay(GpioDisplay):

    def __init__(self, *_args):
        super().__init__(self, *_args)
        GPIO.setup(config.BACKLIGHT_GREEN, GPIO.OUT)
        GPIO.setup(config.BACKLIGHT_BLUE, GPIO.OUT)
        GPIO.setup(config.BACKLIGHT_RED, GPIO.OUT)

    def backlight(self, r, g, b):
        GPIO.output(config.BACKLIGHT_RED,   config.BACKLIGHT_ON if r > 0 else config.BACKLIGHT_OFF)
        GPIO.output(config.BACKLIGHT_GREEN, config.BACKLIGHT_ON if g > 0 else config.BACKLIGHT_OFF)
        GPIO.output(config.BACKLIGHT_BLUE,  config.BACKLIGHT_ON if b > 0 else config.BACKLIGHT_OFF)
