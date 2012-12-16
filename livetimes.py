#!/usr/bin/env python3

import times

# HASLEMERE
STATION = "hsl"

# There can be more than two directions e.g. some stations might have multiple lines going through.
# It's really just a station grouping.
# Could also have things like trains that only go to Guildford are grouped separately.
# Maybe... some way to detect fast and slow trains? (e.g. if it calls at Milford, it's slow)
DIRECTIONS = {
    "London":
    ("London Waterloo",),

    "Portsmouth":
    ("Portsmouth Harbour",
        "Portsmouth & Southsea",
        "Havant",
        "Fratton"),
}

STATION_CODES = {
    'Portsmouth Harbour'    : 'PMH',
    'Portsmouth & Southsea' : 'PMS',
    'London Waterloo'       : 'WAT',
    'Havant'                : 'HAV',
    'Fratton'               : 'FTN',
}

from display import LCDDisplay
lcd = LCDDisplay('/dev/ttyACM0')
lcd.clear()

trains = times.NRETimes(STATION, DIRECTIONS)
for i, direction in enumerate(DIRECTIONS):

    # LCD gets next train in each direction
    next_train = next(trains.going_to(direction))
    time = next_train.departs.strftime("%H:%M")
    lcd.move_to(0, i)
    lcd.write("{0}        {1}".format(time, STATION_CODES[next_train.destination]))

    # Print out all trains in each direction
    print(direction.upper())
    print('-' * len(direction))
    for train in trains.going_to(direction):
        print("{}\t{} {}".format(train.departs.strftime("%H:%M"),
                                 '!' if train.delayed else ' ',
                                 train.destination))

lcd.flush()
