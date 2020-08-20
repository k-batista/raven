from dataclasses import dataclass
from typing import Dict, List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class StockAnalyseDataclass:
    ticker: str
    time_frame: str
    send_message: bool
    client: str

    @classmethod
    def build(cls, ticker, time_frame, send, client):
        return cls(
            ticker=ticker,
            time_frame=time_frame,
            send_message=send,
            client=client
        )


@dataclass_json
@dataclass
class StockIndicatorDataclass:
    ticker: str
    price_open: float
    price_close: float
    price_high: float
    price_low: float
    volume: int
    date: str
    time_frame: str
    variation: float
    indicators: Dict[str, float]

    @classmethod
    def build(cls, request, stock, date, variation, params):

        return cls(
            ticker=request.ticker,
            time_frame=request.time_frame,
            price_open=stock.price_open,
            price_close=stock.price_close,
            price_high=stock.price_high,
            price_low=stock.price_low,
            volume=stock.volume,
            date=date,
            variation=variation,
            indicators=params
        )

    @classmethod
    def from_model(cls, model):
        return cls(
            ticker=model.ticker,
            price_open=model.price_open(),
            price_close=model.price_close(),
            price_high=model.price_high(),
            price_low=model.price_low(),
            volume=model.volume(),
            variation=model.variation(),
            date=model.quote_date,
            time_frame=model.time_frame,
            indicators=model.indicators
        )

    def get_emoji(self):
        return (u"\U0001F534" if self.variation <= 0 else u"\U0001F535")

    def ema_9_emoji(self):
        return (u"\U00002B07" if self.ema_9() <= self.price_close
                else u"\U00002B06")

    def ema_21_emoji(self):
        return (u"\U00002B07" if self.ema_21() <= self.price_close
                else u"\U00002B06")

    def ema_80_emoji(self):
        return (u"\U00002B07" if self.ema_80() <= self.price_close
                else u"\U00002B06")

    def sma_200_emoji(self):
        return (u"\U00002B07" if self.sma_200() <= self.price_close
                else u"\U00002B06")

    def ema_80(self):
        return self.indicators['ema_80']

    def ema_9(self):
        return self.indicators['ema_9']

    def ema_21(self):
        return self.indicators['ema_21']

    def sma_200(self):
        return self.indicators['sma_200']

    def pivot_point(self):
        return self.indicators['pivot']

    def trend(self):
        ema_9 = self.ema_9()
        ema_21 = self.ema_21()
        ema_80 = self.ema_80()

        count_ta = 0
        count_tb = 0

        if ema_9 > ema_21:
            count_ta += 1
        else:
            count_tb += 1

        if self.price_close >= ema_9:
            count_ta += 1
        else:
            count_tb += 1

        if self.price_close >= ema_21:
            count_ta += 1
        else:
            count_tb += 1

        if self.price_close >= ema_80:
            count_ta += 1
        else:
            count_tb += 1

        if count_ta >= 3:
            return 1
        elif count_tb >= 3:
            return -1

        return 0

    def trend_html(self):
        trend_str = ''
        count_trend = self.trend()

        if count_trend == 1:
            trend_str += (f'\n- <b>Tendência: Alta</b> ' + u"\U0001F535")
        elif count_trend == -1:
            trend_str += (f'\n- <b>Tendência: Baixa</b> ' + u"\U0001F534")
        else:
            trend_str += ('\n- <b>Tendência: Indefinida</b> ')

        return trend_str

    def format_stock(self):
        message = ('<b> {0:6}</b> - {13} '
                   '\n- <b>Preço </b> Abr: {1} Fch: {2} [{3} %]'
                   '\n {5} <b>EMA 9</b> = {6:6} '
                   '\n {7} <b>EMA 21</b> = {8:6} '
                   '\n {9} <b>EMA 80</b> = {10:6} '
                   '\n {11} <b>SMA 200</b> = {12:6} '
                   '\n\n- <b>Pivot Point Fibonacci</b>'
                   '\n {14} <b>R3</b> = {17:6} '
                   '\n {14} <b>R2</b> = {18:6} '
                   '\n {14} <b>R1</b> = {19:6} '
                   '\n {15} <b>PP</b> = {20:6} '
                   '\n {16} <b>S1</b> = {21:6} '
                   '\n {16} <b>S2</b> = {22:6} '
                   '\n {16} <b>S3</b> = {23:6} '
                   '\n'
                   .format(self.ticker,
                           self.price_open,
                           self.price_close,
                           self.variation,
                           self.get_emoji(),
                           self.ema_9_emoji(), self.ema_9(),
                           self.ema_21_emoji(), self.ema_21(),
                           self.ema_80_emoji(), self.ema_80(),
                           self.sma_200_emoji(), self.sma_200(),
                           self.date,
                           u"\U00002B06",
                           u"\U000027A1",
                           u"\U00002B07",
                           self.pivot_point()['r3'],
                           self.pivot_point()['r2'],
                           self.pivot_point()['r1'],
                           self.pivot_point()['pp'],
                           self.pivot_point()['s1'],
                           self.pivot_point()['s2'],
                           self.pivot_point()['s3'],))

        return message + self.trend_html()


@dataclass_json
@dataclass
class StockIndicatorListDataclass:
    stocks: List[StockIndicatorDataclass]

    @classmethod
    def build(cls, params):
        stocks = [StockIndicatorDataclass.from_model(p) for p in params]
        return cls(stocks)
