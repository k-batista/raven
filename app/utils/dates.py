from enum import Enum
from datetime import datetime, date
from app.models.types import Months

import pytz


class Timezone(Enum):
    US_EASTERN = pytz.timezone('US/Eastern')


class Format(Enum):
    TICOTICO = '%a, %d %b %Y %H:%M:%S %Z'


def format_current_datetime(date_timezone, date_format):
    date = datetime.now(date_timezone.value)
    return date.strftime(date_format.value)


class MonthUtils:

    def get_abreviate_month_name(monthIndex):
        return Months(monthIndex).name.lower()

    @staticmethod
    def get_diff_in_months_from_today(date_param):
        today = date.today()
        return ((today.year - date_param.year) * 12
                + (today.month - date_param.month))
