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
    if trains.error:
        departures.set_error()
    else:
        departures.set_trains(next_two)


def next_train_in_each_direction():
    next_each = [
        next(trains.going_to(direction))
        for i, direction in enumerate(config.DIRECTIONS)]
    departures.set_trains(next_each)


def all_trains():
    full_list = []
    for i, direction in enumerate(config.DIRECTIONS):
        # Print out all trains in each direction
        #print(direction.upper())
        #print('-' * len(direction))
        for train in trains.going_to(direction):
            full_list.append(train)
    departures.set_trains(full_list)

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
    #next_train_in_each_direction()

    # Don't bother fetching trains between 1am and 5am
    dt = datetime.now()
    if dt.hour in config.QUIET_HOURS:
        hour = config.QUIET_HOURS[-1] + 1
        switch_on = dt.replace(hour=hour, minute=0, second=0)
        sleepytimes = (switch_on - dt).seconds
        print('sleeping until {} ({} seconds)'.format(switch_on, sleepytimes))

    else:
        # Sleep until the next minute boundary
        sleepytimes = (60 - dt.second)

    time.sleep(sleepytimes)
