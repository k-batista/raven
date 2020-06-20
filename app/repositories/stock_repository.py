from sqlalchemy import desc

from .repository_base import RepositoryBase
from app.models.stock import Stock


class StockRepository(RepositoryBase):

    def find_stock_by_ticker_and_date(self, ticker, date):
        with self.app.app_context():
            return (Stock.query.filter_by(
                ticker=ticker,
                des_date=date).first())

    def find_all_stocks_by_ticker(self, ticker):
        with self.app.app_context():
            return (Stock.query.filter_by(ticker=ticker)
                    .order_by(desc(Stock.des_date)).all())
