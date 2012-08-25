#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Yeah I know this is naughty.
# How I wish National Rail would open up their data.
#html = urlopen("http://traintimes.org.uk/live/hsl/").read()
#open("hsl.html", "w").write(html.decode('utf8'))

# HASLEMERE
STATION = "hsl"

# Used to detect past-midnight trains that will be given tomorrow's date
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

        self._arrives = None
        self._departs = None

        self.destination = None
        self.origin = None
        self.platform = None

        self.running = True
        self.delayed = False
        self.starts = False
        self.terminates = False

        self.__parse_row(row)


    @property
    def arrives(self):
        return self._arrives

    @arrives.setter
    def arrives(self, value):
        self._arrives = self.__parse_time(value)

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


    def __parse_stations(self, stations_str):
        stations = [s.strip() for s in stations_str.split('–')]
        if len(stations) >= 2:
            self.origin, self.destination = stations
        elif self.starts:
            self.destination = stations_str
        elif self.terminates:
            if stations_str.startswith("From"):
                stations_str = stations_str[4:].strip()
            self.origin = stations_str

    def __parse_row(self, row):
        times, journey, platform, _ = row

        status = times.pop()
        if status == 'Cancelled':
            self.running = False

        elif status == 'Delayed':
            self.delayed = True

        elif status != 'On time':
            self.delayed = True
            # Put it back... this will be the estimated time
            times.append(status)

        if self.running:

            if len(journey) > 1:
                if journey[1] == 'Starts here':
                    self.starts = True
                    self.departs = times[0]
                elif journey[1] == 'Terminates':
                    self.terminates = True
                    self.arrives = times[0]

            for t in times:
                if t.endswith("a"):
                    self.arrives = t
                elif t.endswith("d"):
                    self.departs = t
                else:
                    self.arrives = self.departs = t

            self.__parse_stations(journey[0])

            if platform:
                self.platform = platform[0]


class TrainTimes(object):

    def __init__(self, station_code):
        self.station_code = station_code

    def __data(self):
        cache = "%s.html" % self.station_code
        html = open(cache).read()
        return BeautifulSoup(html)

    def __trains(self):
        for row in self.__data().find(id="content").table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) > 3:
                yield Train([list(td.strings) for td in cells])
    
    def trains(self):
        return [t for t in self.__trains() if t.running]

    def departing(self):
        now = datetime.now()
        return [t for t in self.trains() if not t.terminates and t.departs > now]

    def arriving(self):
        return [t for t in self.trains() if not t.starts]

    def going_to(self, direction):
        """Return all trains going in a particular direction"""
        return [t for t in self.departing() if t.direction.lower() == direction.lower()]


traintimes = TrainTimes(STATION)
for direction in DIRECTIONS:
    print(direction.upper())
    print('-'*len(direction))
    for train in traintimes.going_to(direction):
        print("{}\t{} {}".format(train.departs.strftime("%H:%M"), '!' if train.delayed else ' ', train.destination))
    print()
