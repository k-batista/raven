from sqlalchemy.dialects.postgresql import JSONB

from .base import db, Base


class Stock(Base):
    __tablename__ = 'stock'

    id_stock = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    time_frame = db.Column(db.String, nullable=False)
    quote_date = db.Column(db.String, nullable=False)
    quote = db.Column(JSONB, nullable=False)
    indicators = db.Column(JSONB, nullable=False)

    @classmethod
    def from_dataclass(cls, dataclass):
        return cls(
            ticker=dataclass.ticker,
            time_frame=dataclass.time_frame,
            quote_date=dataclass.date,
            quote={'price_open': dataclass.price_open,
                   'price_close': dataclass.price_close,
                   'price_high': dataclass.price_high,
                   'price_low': dataclass.price_low,
                   'variation': dataclass.variation,
                   'volume': dataclass.volume},
            indicators=dataclass.indicators
        )

    def price_open(self):
        return self.quote['price_open']

    def price_close(self):
        return self.quote['price_close']

    def price_high(self):
        return self.quote['price_high']

    def price_low(self):
        return self.quote['price_low']

    def variation(self):
        return self.quote['variation']

    def volume(self):
        return self.quote['volume']

    def ema_80(self):
        return self.indicators['ema_80']

    def ema_9(self):
        return self.indicators['ema_9']

    def ema_21(self):
        return self.indicators['ema_21']

    def sma_200(self):
        return self.indicators['sma_200']
