from dataclasses import dataclass
from typing import Dict, List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class StockAnalyse:
    ticker: str
    send_message: bool

    @classmethod
    def build(cls, ticker, send):
        return cls(
            ticker=ticker,
            send_message=send
        )


@dataclass_json
@dataclass
class StockIndicators:
    ticker: str
    price_open: float
    price_close: float
    price_high: float
    price_low: float
    volume: int
    date: str
    variation: float
    indicators: Dict[str, float]

    @classmethod
    def build(cls, ticker, stock, date, variation, params):

        return cls(
            ticker=ticker,
            price_open=stock.price_open,
            price_close=stock.price_close,
            price_high=stock.price_high,
            price_low=stock.price_low,
            volume=stock.volume,
            variation=variation,
            date=date,
            indicators=params
        )

    @classmethod
    def from_model(cls, model):
        return cls(
            ticker=model.ticker,
            price_open=model.price_open,
            price_close=model.price_close,
            price_high=model.price_high,
            price_low=model.price_low,
            volume=model.volume,
            variation=model.variation,
            date=model.des_date,
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


@dataclass_json
@dataclass
class StockIndicatorsList:
    stocks: List[StockIndicators]

    @classmethod
    def build(cls, params):
        stocks = [StockIndicators.from_model(p) for p in params]
        return cls(stocks)
