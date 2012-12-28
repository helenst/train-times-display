import config
import display
import formats


class DepartureBoard:

    def __init__(self):
        self.display = config.DISPLAY()
        self.formatter = config.FORMATTER()
        self.display.clear()

    def display_train(self, train, row):
        self.display.move_to(0, row)
        self.display.write(self.formatter.output(train))
