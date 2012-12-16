#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# HASLEMERE
STATION = "hsl"

# Detect past-midnight trains that will be given tomorrow's date
DAY_CUTOFF = 4

# There can be more than two directions e.g. some stations might have multiple lines going through.
# It's really just a station grouping.
# Could also have things like trains that only go to Guildford are grouped separately.
# Maybe... some way to detect fast and slow trains? (e.g. if it calls at Milford, it's slow)

DIRECTIONS = {
    "London":
        ("London Waterloo"),

    "Portsmouth":
        ("Portsmouth Harbour",
         "Portsmouth & Southsea",
         "Havant",
         "Fratton"),
}

class Train(object):

    def __init__(self, row):

        # managed by property
        self._departs = None

        self.destination = None
        self.platform = None

        self.running = True
        self.delayed = False

        self.__parse_row(row)

    @property
    def departs(self):
        return self._departs

    @departs.setter
    def departs(self, value):
        self._departs = self.__parse_time(value)

    @property
    def direction(self):
        for name, destinations in DIRECTIONS.items():
            if self.destination in destinations:
                return name


    def __parse_time(self, hhmm):
        time = datetime.strptime(hhmm.strip().strip("ad"), "%H:%M").time()
        day = datetime.today()

        # Looking across the midnight boundary, use tomorrow's date
        if time.hour < DAY_CUTOFF and not now.hour < DAY_CUTOFF:
            day += timedelta(days=1)

        return datetime.combine(day, time)

    def __parse_row(self, row):
        # ROW: due time, destination, status, platform, details
        due, destination, status, platform, _ = row

        self.destination = destination[0].strip()
        self.departs = due[0]
        self.platform = platform[0] if platform else ''
        status = status[0]

        if status == 'Cancelled':
            self.running = False

        elif status == 'Delayed':
            self.delayed = True

        elif status != 'On time':
            self.delayed = True
            # TODO: read in expected time


class NRETimes(object):

    def __init__(self, station_code):
        self.station_code = station_code

    def live_doc(self):
        # Yeah, scraping is naughty. Open up your data, NRE!
        nre_url = "http://ojp.nationalrail.co.uk/service/ldbboard/dep/%s" % \
                  self.station_code.upper()
        html = urlopen(nre_url).read()
        return BeautifulSoup(html)
        #open("nre_hsl.html", "w").write(html.decode('utf8'))

    def doc(self):
        cache = "nre_%s.html" % self.station_code
        html = open(cache).read()
        return BeautifulSoup(html)

    def trains(self):
        for row in self.doc().find('table').tbody.find_all('tr'):
            cells = row.find_all("td")
            yield Train([list(td.strings) for td in cells])

    def departing(self):
        now = datetime.now()
        return [t for t in self.trains() if t.running and t.departs > now]

    def going_to(self, direction):
        """Return all trains going in a particular direction"""
        return [t for t in self.departing() if t.direction.lower() == direction.lower()]


traintimes = NRETimes(STATION)
for direction in DIRECTIONS:
    print(direction.upper())
    print('-'*len(direction))
    for train in traintimes.going_to(direction):
        print("{}\t{} {}".format(train.departs.strftime("%H:%M"), '!' if train.delayed else ' ', train.destination))
    print()
