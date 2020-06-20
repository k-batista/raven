from dateutil.relativedelta import relativedelta
from datetime import date, datetime


def get_end_trading_day():
    today = date.today()
    now = datetime.now()

    if today.weekday() == 5:
        today += relativedelta(days=-1)
    elif today.weekday() == 6:
        today += relativedelta(days=-2)

    return (get_business_day(today)
            if now.hour >= 18
            else get_business_day(today, days=1))


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
    '2019-11-15', '2019-12-25', '2020-01-01', '2020-02-24', '2020-02-25',
    '2020-04-10', '2020-04-21', '2020-05-01', '2020-06-11', '2020-09-07',
    '2020-10-12', '2020-11-02', '2020-11-15', '2020-12-25', '2021-01-01',
    '2021-02-15', '2021-02-16', '2021-04-02', '2021-04-21', '2021-05-01',
    '2021-06-03', '2021-09-07', '2021-10-12', '2021-11-02', '2021-11-15',
    '2021-12-25', '2022-01-01', '2022-02-28', '2022-03-01', '2022-04-15',
    '2022-04-21', '2022-05-01', '2022-06-16', '2022-09-07', '2022-10-12',
    '2022-11-02', '2022-11-15', '2022-12-25', '2023-01-01', '2023-02-20',
    '2023-02-21', '2023-04-07', '2023-04-21', '2023-05-01', '2023-06-08',
    '2023-09-07', '2023-10-12', '2023-11-02', '2023-11-15', '2023-12-25',
    '2024-01-01', '2024-02-12', '2024-02-13', '2024-03-29', '2024-04-21',
    '2024-05-01', '2024-05-30', '2024-09-07', '2024-10-12', '2024-11-02',
    '2024-11-15', '2024-12-25', '2025-01-01', '2025-03-03', '2025-03-04',
    '2025-04-18', '2025-04-21', '2025-05-01', '2025-06-19', '2025-09-07',
    '2025-10-12', '2025-11-02', '2025-11-15', '2025-12-25', '2026-01-01',
    '2026-02-16', '2026-02-17', '2026-04-03', '2026-04-21', '2026-05-01',
    '2026-06-04', '2026-09-07', '2026-10-12', '2026-11-02', '2026-11-15',
    '2026-12-25', '2027-01-01', '2027-02-08', '2027-02-09', '2027-03-26',
    '2027-04-21', '2027-05-01', '2027-05-27', '2027-09-07', '2027-10-12',
    '2027-11-02', '2027-11-15', '2027-12-25', '2028-01-01', '2028-02-28',
    '2028-02-29', '2028-04-14', '2028-04-21', '2028-05-01', '2028-06-15',
    '2028-09-07', '2028-10-12', '2028-11-02', '2028-11-15', '2028-12-25',
    '2029-01-01', '2029-02-12', '2029-02-13', '2029-03-30', '2029-04-21',
    '2029-05-01', '2029-05-31', '2029-09-07', '2029-10-12', '2029-11-02',
    '2029-11-15', '2029-12-25', '2030-01-01', '2030-03-04', '2030-03-05',
    '2030-04-19', '2030-04-21', '2030-05-01', '2030-06-20', '2030-09-07',
    '2030-10-12', '2030-11-02', '2030-11-15', '2030-12-25',

    # Sao Paulo holidays
    '2019-07-09', '2019-11-20', '2020-01-25', '2020-07-09', '2020-11-20',
    '2021-01-25', '2021-07-09', '2021-11-20', '2022-01-25', '2022-07-09',
    '2022-11-20', '2023-01-25', '2023-07-09', '2023-11-20',
))

get_end_trading_day()
