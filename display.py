import serial

class LCDDisplay(object):

    def __init__(self, device, rate=9600, cols=16, rows=2):
        self.port = serial.Serial(device, rate)
        self.cols = cols
        self.rows = rows

    def clear(self):
        self.port.write('c'.encode())

    def move_to(self, col, row):
        self.port.write(bytearray([ord('m'), col, row]))

    def write(self, string):
        self.port.write('w{0}\0'.format(string).encode())

    def flush(self):
        self.port.flush()
