
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

SERIAL_PORT = '/dev/ttyACM0'

import display
DISPLAY = display.SerialDisplay

import formats
FORMATTER = formats.SixteenByTwo
