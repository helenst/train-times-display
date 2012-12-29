#!/usr/bin/env python3

import itertools

import times
import config

from board import DepartureBoard
departures = DepartureBoard()


def fetch_data():
    return times.NRETimes(config.STATION, config.DIRECTIONS)

trains = fetch_data()


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

from datetime import datetime
import time

# wait two seconds for arduino to reset
print("starting up...", end=" ")
time.sleep(2)
print("OK")

while True:

    # update data every 5 minutes
    minute = datetime.now().minute
    if minute % 5 == 0:
        trains = fetch_data()

    next_two_to_waterloo()

    # Sleep until the next minute boundary
    s = datetime.now().second
    time.sleep(60 - s)
