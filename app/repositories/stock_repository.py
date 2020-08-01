from sqlalchemy import desc

from .repository_base import RepositoryBase
from app.models.stock import Stock


class StockRepository(RepositoryBase):

    def find_stock_by_ticker_and_timeframe_and_date(
            self, ticker, time_frame, date):
        with self.app.app_context():
            return (Stock.query.filter_by(
                ticker=ticker,
                time_frame=time_frame,
                quote_date=date).first())

    def find_all_stocks_by_ticker(self, ticker, time_frame):
        with self.app.app_context():
            return (Stock.query.filter_by(ticker=ticker,
                                          time_frame=time_frame)
                    .order_by(desc(Stock.quote_date)).all())

    def find_all_tickers(self):
        with self.app.app_context():
            return (self.session().query(Stock.ticker).distinct()
                    .order_by(Stock.ticker).all())
