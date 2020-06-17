from dataclasses import dataclass
from typing import Dict

from dataclasses_json import dataclass_json


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
    indicators: Dict[str, float]

    @classmethod
    def build(cls, ticker, stock, date, params):
        return cls(
            ticker=ticker,
            price_open=stock['1. open'],
            price_close=stock['4. close'],
            price_high=stock['2. high'],
            price_low=stock['2. high'],
            volume=stock['5. volume'],
            date=date,
            indicators=params
        )
