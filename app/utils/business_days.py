import time
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from app.models.types import TimeFrame

def get_last_week_business_day(date):
    if date.weekday() != 5:
        while date.weekday() != 5:
            date += relativedelta(days=-1)
    
    return get_business_day(date)

def get_end_trading_day(time_frame):

    today = date.today()
    now = datetime.now()

    if time_frame == TimeFrame.weekly.value:
        return get_last_week_business_day(today)


    if today.weekday() in (5, 6):
        while not _is_business_day(today):
            today += relativedelta(days=-1)

        return today

    return (get_business_day(today)
            if now.hour >= 18
            else get_business_day(today, days=-1))


def get_timestamp(date):
    return int(
        time.mktime(
            time.strptime(
                f'{date.year}-{date.month}-{date.day} 13:00:00',
                '%Y-%m-%d %H:%M:%S')))


def get_business_day(today, days=0):
    if days == 0:
        while not _is_business_day(today):
            today += relativedelta(days=-1)

        return today

    if days > 0:
        increment = 1
    else:
        increment = -1

    n = abs(days)

    while n:
        today += relativedelta(days=increment)
        while not _is_business_day(today):
            today += relativedelta(days=increment)
        n -= 1

    return today


def _is_business_day(date):
    # monday is 0, sunday is 6
    return True if (date.weekday() not in (5, 6)
                    and date not in HOLIDAYS) else False


# Helpers for parsing the result of isoformat()
def _parse_isoformat_date(dtstr):
    # It is assumed that this function will only be called with a
    # string of length exactly 10, and (though this is not used) ASCII-only
    year = int(dtstr[0:4])
    if dtstr[4] != '-':
        raise ValueError('Invalid date separator: %s' % dtstr[4])

    month = int(dtstr[5:7])

    if dtstr[7] != '-':
        raise ValueError('Invalid date separator')

    day = int(dtstr[8:10])

    return date(year, month, day)


HOLIDAYS = frozenset(_parse_isoformat_date(d) for d in (
    '2017-01-01', '2017-01-25', '2017-02-24', '2017-02-25', '2017-04-10',
    '2017-04-21', '2017-05-01', '2017-06-11', '2017-07-09', '2017-09-07',
    '2017-11-20', '2017-12-25',
    '2018-01-01', '2018-01-25', '2018-02-24', '2018-02-25', '2018-04-10',
    '2018-04-21', '2018-05-01', '2018-06-11', '2018-07-09', '2018-09-07',
    '2018-11-20', '2018-12-25',
    '2019-01-01', '2019-01-25', '2019-02-24', '2019-02-25', '2019-04-10',
    '2019-04-21', '2019-05-01', '2019-06-11', '2019-07-09', '2019-09-07',
    '2019-11-20', '2019-12-25',
    '2020-01-01', '2020-01-25', '2020-02-24', '2020-02-25', '2020-04-10',
    '2020-04-21', '2020-05-01', '2020-06-11', '2020-07-09', '2020-09-07',
    '2020-10-12', '2020-11-20', '2020-12-25',
    '2021-01-01', '2021-01-25', '2021-02-24', '2021-02-25', '2021-04-10',
    '2021-04-21', '2021-05-01', '2021-06-11', '2021-07-09', '2021-09-07',
    '2021-11-20', '2011-12-25'

))

