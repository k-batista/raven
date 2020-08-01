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
        quote_date = str(datetime.fromtimestamp(timestamp).date())
        price_open = quotes['open'][index]
        price_close = quotes['close'][index]
        price_high = quotes['high'][index]
        price_low = quotes['low'][index]
        volume = quotes['volume'][index]

        if not price_open:
            price_open = price_close

        if not price_close:
            return None

        return cls(
            ticker=ticker,
            price_open=round(float(price_open), 2),
            price_close=round(float(price_close), 2),
            price_high=round(float(price_high), 2),
            price_low=round(float(price_low), 2),
            volume=int(volume),
            date=quote_date
        )

    @classmethod
    def from_alphavantage(cls, ticker, stock, date):

        return cls(
            ticker=ticker,
            price_open=round(float(stock['1. open']), 2),
            price_close=round(float(stock['4. close']), 2),
            price_high=round(float(stock['2. high']), 2),
            price_low=round(float(stock['3. low']), 2),
            volume=int(stock['5. volume']),
            date=date,
        )
