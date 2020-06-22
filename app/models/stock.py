from sqlalchemy.dialects.postgresql import JSONB

from .base import db, Base


class Stock(Base):
    __tablename__ = 'stock'

    id_stock = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    price_open = db.Column(db.Numeric(12, 2), nullable=False)
    price_close = db.Column(db.Numeric(12, 2), nullable=False)
    price_high = db.Column(db.Numeric(12, 2), nullable=False)
    price_low = db.Column(db.Numeric(12, 2), nullable=False)
    variation = db.Column(db.Numeric(12, 2), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
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
            variation=dataclass.variation,
            volume=dataclass.volume,
            des_date=dataclass.date,
            indicators=dataclass.indicators
        )

    def ema_80(self):
        return self.indicators['ema_80']

    def ema_9(self):
        return self.indicators['ema_9']

    def ema_21(self):
        return self.indicators['ema_21']

    def sma_200(self):
        return self.indicators['sma_200']
