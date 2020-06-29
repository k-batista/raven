from datetime import datetime

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class QuoteDataclass:
    ticker: str
    price_open: float
    price_close: float
    price_high: float
    price_low: float
    volume: int
    date: str

    @classmethod
    def from_yahoo(cls, ticker, quotes, index, timestamp):
        des_date = str(datetime.fromtimestamp(timestamp).date())
        price_open = quotes['open'][index]
        price_close = quotes['close'][index]
        price_high = quotes['high'][index]
        price_low = quotes['low'][index]
        volume = quotes['volume'][index]

        if not price_open or not price_close:
            return None

        return cls(
            ticker=ticker,
            price_open=float(price_open),
            price_close=float(price_close),
            price_high=float(price_high),
            price_low=float(price_low),
            volume=int(volume),
            date=des_date
        )

    @classmethod
    def from_alphavantage(cls, ticker, stock, date):

        return cls(
            ticker=ticker,
            price_open=float(stock['1. open']),
            price_close=float(stock['4. close']),
            price_high=float(stock['2. high']),
            price_low=float(stock['3. low']),
            volume=int(stock['5. volume']),
            date=date,
        )
