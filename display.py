import serial


class DeviceTimeoutError(Exception):
    pass


class Display(object):

    def __init__(self, device, rate=9600, cols=16, rows=2):
        self.port = serial.Serial(device, rate, timeout=10)
        self.wait_for_ready()
        self.cols = cols
        self.rows = rows

    # Serial connection resets arduino.
    # Wait for this to complete (send a zero) before pushing any data
    def wait_for_ready(self):
        data = self.port.read()
        if data[0] == 0:
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

    def flush(self):
        self.port.flush()
