
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Detect past-midnight trains that will be given tomorrow's date
DAY_CUTOFF = 4

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

    def will_depart(self):
        return self.running and self.departs > datetime.now()

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
        cache = "nre_%s.html" % self.station_code
        html = open(cache).read()
        return BeautifulSoup(html)

    def trains(self):
        for row in self.live_doc().find('table').tbody.find_all('tr'):
            cells = row.find_all("td")
            yield Train([list(td.strings) for td in cells])

    def departing(self):
        return (t for t in self.trains() if t.will_depart())

    def going_to(self, direction):
        """Return all trains going in a particular direction"""
        destinations = [d.lower() for d in self.directions[direction]]
        return (t for t in self.departing() if t.destination.lower() in destinations)
