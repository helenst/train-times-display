#!/usr/bin/env python3

import itertools

import times
import config

from display import LCDDisplay
lcd = LCDDisplay(config.SERIAL_PORT)
lcd.clear()

trains = times.NRETimes(config.STATION, config.DIRECTIONS)


def next_two_to_waterloo():

    next_two = itertools.islice(trains.going_to("London"), 0, 2, 1)
    for i, train in enumerate(next_two):
        time = train.timetabled_departure.strftime("%H:%M")

        minutes = train.minutes_until
        if minutes is None:
            minutes = '??'  # Expected departure unknown
        elif minutes > 99:
            minutes = '--'  # A long time until this train leaves

        if train.delayed:
            if train.minutes_late:
                delay = '+{}'.format(train.minutes_late)  # Known delay
            else:
                delay = '!'                               # Unknown delay
        else:
            delay = ''

        lcd.move_to(0, i)
        lcd.write("{time} {countdown:2} {delay:>3} {station}".format(
            time=time,
            countdown=minutes,
            delay=delay,
            station=config.STATION_CODES[train.destination]))


def next_train_in_each_direction():
    for i, direction in enumerate(config.DIRECTIONS):
        # LCD gets next train in each direction
        next_train = next(trains.going_to(direction))
        time = next_train.timetabled_departure.strftime("%H:%M")
        lcd.move_to(0, i)
        lcd.write("{time} {countdown:2} {delay:>3}  {station}".format(
            time=time,
            countdown=next_train.minutes_until,
            delay=next_train.minutes_late or '',
            station=config.STATION_CODES[next_train.destination]))


def all_trains_to_console():
    for i, direction in enumerate(config.DIRECTIONS):
        # Print out all trains in each direction
        print(direction.upper())
        print('-' * len(direction))
        for train in trains.going_to(direction):
            print("{}\t{}{} {}".format(
                train.timetabled_departure.strftime("%H:%M"),
                '!' if train.delayed else ' ',
                train.actual_departure.strftime("%H:%M") if train.actual_departure else '??:??',
                train.destination))

next_two_to_waterloo()

lcd.flush()
