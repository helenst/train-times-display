import config

class Full:
    def output(self, train):
        return ("{time}\t{delayed}{actual} {destination}".format(
            time=train.timetabled_departure.strftime("%H:%M"),
            delayed='!' if train.delayed else ' ',
            actual=train.actual_departure.strftime("%H:%M") if train.actual_departure else '??:??',
            destination=train.destination))


class SixteenByTwo:

    @classmethod
    def countdown(cls, train):

        minutes = train.minutes_until
        if minutes is None:
            minutes = '??'  # Expected departure unknown
        elif minutes > 99:
            minutes = '99'  # A long time until this train leaves
        return str(minutes)

    @classmethod
    def delay(cls, train):
        if train.delayed:
            if train.minutes_late:
                return '+{}'.format(train.minutes_late)  # Known delay
            else:
                return '!'                               # Unknown delay
        else:
            return ''

    def output(self, train):

        time = train.timetabled_departure.strftime("%H:%M")
        return "{time} {countdown:2} {delay:>3} {station}".format(
            time=time,
            countdown=self.__class__.countdown(train),
            delay=self.__class__.delay(train),
            station=config.STATION_CODES[train.destination])
