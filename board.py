import config
import display
import formats


class DepartureBoard:

    STATE_DELAY, STATE_OK, STATE_INACTIVE = range(0,3)

    def __init__(self):
        self.display = config.DISPLAY()
        self.display.backlight(0, 1, 0)
        self.formatter = config.FORMATTER()
        self.delayed = {}
        self.display.clear()

    def set_trains(self, trains):
        self.display.clear()
        for i, train in enumerate(trains):
            self.display_train(train, i)

        if trains:
            if any([t.delayed for t in trains]):
                self.set_state(self.STATE_ERROR)
            else:
                self.set_state(self.STATE_OK)
        else:
            self.display.move_to(0, 0)
            self.display.write('***   GOOD   ***')
            self.display.move_to(0, 1)
            self.display.write('***   NIGHT  ***')
            self.set_state(self.STATE_INACTIVE)

    def set_state(self, state):
        """Set the state of the board
        OK means everything is running as usual
        DELAYED means one or more trains is delayed
        INACTIVE means no trains in the system (probably night time)
        """
        if state == self.STATE_DELAY:
             # TODO: redness
            self.display.backlight(0, 0, 1)
        elif state == self.STATE_OK:
            self.display.backlight(0, 1, 0)
        elif state == self.STATE_INACTIVE:
            self.display.backlight(0, 0, 0)

    def display_train(self, train, row):
        """Write a single train to the board"""
        self.display.move_to(0, row)
        self.display.write(self.formatter.output(train))
