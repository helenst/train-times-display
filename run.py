#!/usr/bin/env python3

import itertools

import times
import config

from board import DepartureBoard
departures = DepartureBoard()

trains = times.NRETimes(config.STATION, config.DIRECTIONS)

# may need running if the arduino is manually reset
# import time
# time.sleep(3)


def next_two_to_waterloo():

    next_two = itertools.islice(trains.going_to("London"), 0, 2, 1)
    for i, train in enumerate(next_two):
        departures.display_train(train, i)


def next_train_in_each_direction():
    for i, direction in enumerate(config.DIRECTIONS):
        # LCD gets next train in each direction
        next_train = next(trains.going_to(direction))
        departures.display_train(next_train, i)


def all_trains():
    for i, direction in enumerate(config.DIRECTIONS):
        # Print out all trains in each direction
        #print(direction.upper())
        #print('-' * len(direction))
        for train in trains.going_to(direction):
            departures.display_train(train, i)

next_two_to_waterloo()
