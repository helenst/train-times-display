import config
import serial

class DeviceTimeoutError(Exception):
    pass


class DummyDisplay:

    def __init__(self, *args):
        pass

    def write(self, string):
        print(string)

    def move_to(self, row, col):
        print("move to {}, {}".format(row, col))

    def clear(self):
        print("clear")


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
