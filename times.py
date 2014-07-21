from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import config

# Detect past-midnight trains that will be given tomorrow's date
DAY_CUTOFF = 4


class Train(object):

    def __init__(self, row):

        # managed by property
        self._timetabled_departure = None
        self._actual_departure = None

        self.destination = None
        self.platform = None

        self.running = True
        self.delayed = False
        self.minutes_late = None

        self.__parse_row(row)

    @property
    def timetabled_departure(self):
        return self._timetabled_departure

    @timetabled_departure.setter
    def timetabled_departure(self, value):
        self._timetabled_departure = self.__parse_time(value)

    @property
    def actual_departure(self):
        return self._actual_departure

    @actual_departure.setter
    def actual_departure(self, value):
        self._actual_departure = self.__parse_time(value)

    @property
    def unknown_delay(self):
        return self.delayed and self.minutes_late is None

    @property
    def severely_delayed(self):
        return self.delayed and (
                self.unknown_delay or
                self.minutes_late >= config.SEVERE_DELAY_THRESHOLD)

    @property
    def minutes_until(self):
        if self.actual_departure:
            return int((self.actual_departure - datetime.now()).total_seconds() / 60)

    def __str__(self):
        return "{0} to {1}".format(
                self.timetabled_departure.strftime("%H:%M"),
                self.destination)

    def will_depart(self):
        return self.running and (
            self.actual_departure is None or
            self.actual_departure > datetime.now())

    def __parse_time(self, hhmm):
        time = datetime.strptime(hhmm.strip().strip("ad"), "%H:%M").time()
        day = datetime.today()
        now = datetime.now()

        # Looking across the midnight boundary, use tomorrow's date
        if time.hour < DAY_CUTOFF and not now.hour < DAY_CUTOFF:
            day += timedelta(days=1)

        return datetime.combine(day, time)

    def __parse_row(self, row):
        # ROW: due time, destination, status, platform, details
        due, destination, status, platform, _ = row

        self.destination = destination[0].strip()
        self.timetabled_departure = due[0]
        self.platform = platform[0] if platform else ''
        status = [s.strip() for s in status]

        if 'Cancelled' in status:
            self.running = False

        elif 'late' in status or 'Delayed' in status:
            self.delayed = True

            # Read in expected time
            try:
                self.actual_departure = status[0]
                self.minutes_late = int(status[2])
            except (ValueError, KeyError):
                pass

        else:
            # On time
            self._actual_departure = self._timetabled_departure


class NRETimes(object):

    def __init__(self, station_code, directions):
        self.station_code = station_code
        self.directions = directions

    def live_doc(self):
        # Yeah, scraping is naughty. Open up your data, NRE!
        nre_url = "http://ojp.nationalrail.co.uk/service/ldbboard/dep/%s" % \
                  self.station_code.upper()
        html = urlopen(nre_url).read()
        return BeautifulSoup(html)
        #open("nre_hsl.html", "w").write(html.decode('utf8'))

    def doc(self):
        cache = "data/nre_%s.html" % self.station_code
        html = open(cache).read()
        return BeautifulSoup(html)

    def trains(self):
        try:
            table = self.live_doc().find('table')
            if table:
                for row in table.tbody.find_all('tr'):
                    cells = row.find_all("td")
                    yield Train([list(td.strings) for td in cells])
        except Exception as e:
            import traceback
            traceback.print_exc()

    def departing(self):
        return (t for t in self.trains() if t.will_depart())

    def going_to(self, direction):
        """Return all trains going in a particular direction"""
        destinations = [d.lower() for d in self.directions[direction]]
        return (t for t in self.departing() if t.destination.lower() in destinations)
