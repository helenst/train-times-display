import config
import display
import formats


class DepartureBoard:

    STATE_DELAY, STATE_OK, STATE_INACTIVE = range(0,3)

    def __init__(self):
        self.display = config.DISPLAY()
        self.display.backlight(0, 1, 0)
        self.formatter = config.FORMATTER()
        self.display.clear()
        self.current_trains = []

    def set_trains(self, trains):
        trains = list(trains)

        for i, train in enumerate(trains):
            self.display_train(train, i)

        for i in range(len(trains),len(self.current_trains)):
            self.display_row(' '*16, i)

        self.current_trains = trains

        if trains:
            if any([t.delayed for t in trains]):
                self.set_state(self.STATE_DELAY)
            else:
                self.set_state(self.STATE_OK)
        else:
            self.set_state(self.STATE_INACTIVE)

    def set_state(self, state):
        """Set the state of the board
        OK means everything is running as usual
        DELAYED means one or more trains is delayed
        INACTIVE means no trains in the system (probably night time)
        """
        if state == self.STATE_DELAY:
            # Red
            self.display.backlight(1, 0, 0)
        elif state == self.STATE_OK:
            # Green
            self.display.backlight(0, 1, 0)
        elif state == self.STATE_INACTIVE:
            # Lights out
            self.display_row('***   GOOD   ***', 0)
            self.display_row('***   NIGHT  ***', 1)
            self.display.backlight(0, 0, 0)

    def display_row(self, text, row):
        """Write a single line of text to the board"""
        print(text, row)
        self.display.move_to(0, row)
        self.display.write(text)

    def display_train(self, train, row):
        """Write a single train to the board"""
        self.display_row(self.formatter.output(train), row)
