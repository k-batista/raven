from sqlalchemy.dialects.postgresql import JSONB
from chrononaut import Versioned

from .base import db, Base


class Stock(Base, Versioned):
    __tablename__ = 'stock'

    id_stock = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    price_open = db.Column(db.Numeric(12, 2), nullable=False)
    price_close = db.Column(db.Numeric(12, 2), nullable=False)
    price_high = db.Column(db.Numeric(12, 2), nullable=False)
    price_low = db.Column(db.Numeric(12, 2), nullable=False)
    des_date = db.Column(db.String, nullable=False)
    indicators = db.Column(JSONB, nullable=False)

    @classmethod
    def from_dataclass(cls, dataclass):
        return cls(
            ticker=dataclass.ticker,
            price_open=dataclass.price_open,
            price_close=dataclass.price_close,
            price_high=dataclass.price_high,
            price_low=dataclass.price_low,
            des_date=dataclass.date,
            indicators=dataclass.indicators
        )

    def get_var(self, stock_old):
        return round(
            (((self.price_close * 100) / stock_old.price_close) - 100), 2)

    def get_emoji(self, stock_old):
        return (u"\U0001F534" if self.get_var(
            stock_old) <= 0 else u"\U0001F535")
