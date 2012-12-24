#!/usr/bin/env python3

import times
import config

from display import LCDDisplay
lcd = LCDDisplay(config.SERIAL_PORT)
lcd.clear()

trains = times.NRETimes(config.STATION, config.DIRECTIONS)
for i, direction in enumerate(config.DIRECTIONS):

    # LCD gets next train in each direction
    next_train = next(trains.going_to(direction))
    time = next_train.timetabled_departure.strftime("%H:%M")
    lcd.move_to(0, i)
    lcd.write("{0}        {1}".format(time, config.STATION_CODES[next_train.destination]))

    # Print out all trains in each direction
    print(direction.upper())
    print('-' * len(direction))
    for train in trains.going_to(direction):
        print("{}\t{}{} {}".format(
                train.timetabled_departure.strftime("%H:%M"),
                '!' if train.delayed else ' ',
                train.actual_departure.strftime("%H:%M") if train.actual_departure else '??:??',
                train.destination))

lcd.flush()
