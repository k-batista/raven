from collections import OrderedDict

from app.clients.quote_client import get_client
from app.dataclass.stock_dataclass import StockAnalyseDataclass


class StockIndicator:

    def __init__(self, params: StockAnalyseDataclass, date):
        self.get_prices = get_client(params.client)
        self.params = params
        self.date = date
        self.emas = {}
        self.__prices()

    def __prices(self):
        response = self.get_prices(self.params, self.date, True)

        self.prices = OrderedDict(sorted(response.items()))
        self.reverse_prices = OrderedDict(
            sorted(response.items(), reverse=True))

    def get_price_by_date(self, date):
        return self.prices.get(str(date))

    def get_sma(self, period, date):

        count = 0
        average = 0

        for key, value in self.reverse_prices.items():
            if count == period:
                break

            if key == date or count > 0:
                count += 1
                average += value.price_close

        return round(average / period, 2)

    def __ema(self, period):

        emas = self.emas.get(f'ema_{period}')
        if emas:
            return emas

        emas = {}
        count = 1
        average = 0
        multiplier = 2 / (period + 1)

        for key, value in self.prices.items():

            value = value.price_close

            if count < period:
                average += value
                count += 1
                continue
            elif count == period:
                average = average / (period - 1)
                count += 1

            ema = round((((value - average) * multiplier) + average), 2)
            emas[key] = ema
            average = ema

        self.emas[f'ema_{period}'] = emas

        return emas

    def get_ema(self, period, date):
        emas = self.__ema(period)

        return emas.get(date)

    def generate_pivot_point(self, quotation_date):
        quote = self.get_price_by_date(quotation_date)

        pp = round(
            (quote.price_close +
             quote.price_low +
             quote.price_high) /
            3,
            2)
        high_less_low = (quote.price_high - quote.price_low)
        r3 = round(pp + high_less_low, 2)
        r2 = round(pp + (high_less_low * 0.618), 2)
        r1 = round(pp + (high_less_low * 0.382), 2)

        s1 = round(pp - (high_less_low * 0.382), 2)
        s2 = round(pp - (high_less_low * 0.618), 2)
        s3 = round(pp - high_less_low, 2)

        return dict(
            pivot=dict(
                pp=pp,
                r3=r3,
                r2=r2,
                r1=r1,
                s1=s1,
                s2=s2,
                s3=s3))
