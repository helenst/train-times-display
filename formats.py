import config


class Full:

    def output(self, train):
        """Format train information for a terminal display"""

        return ("{time}\t{delayed}{actual} {destination}".format(
            time=train.timetabled_departure.strftime("%H:%M"),
            delayed='!' if train.delayed else ' ',
            actual=train.actual_departure.strftime("%H:%M") if train.actual_departure else '??:??',
            destination=train.destination))


class SixteenByTwo:

    def countdown(self, train):
        """Indicate number of minutes until train departs
           Unknown departure time:     '??'
           More than 99 minutes away:  '99'
           Fewer than 99 minutes away: '37'
        """

        minutes = train.minutes_until
        if minutes is None:
            minutes = '??'  # Expected departure unknown
        elif minutes > 99:
            minutes = '99'  # A long time until this train leaves
        return str(minutes)

    def delay(self, train):
        """Indicate number of minutes the train is delayed
            Known delay:   '+37'
            Unknown delay: '!'
            No delay:      ''
        """

        if train.delayed:
            if train.minutes_late:
                return '+{}'.format(train.minutes_late)  # Known delay
            else:
                return '!'                               # Unknown delay
        else:
            return ''

    def output(self, train):
        """Format train information for a 16x2 character display
            Normal (no delay):  10:32 10     WAT
            Known delay:        10:47  8 +35 PMH
            Unknown delay:      11:01 ??   ! RDG
        """

        time = train.timetabled_departure.strftime("%H:%M")
        return "{time} {countdown:2} {delay:>3} {station}".format(
            time=time,
            countdown=self.countdown(train),
            delay=self.delay(train),
            station=config.STATION_CODES[train.destination])
