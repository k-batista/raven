import logging

from app.config.app_context import ApplicationContext
from app.utils.business_days import get_end_trading_day
from app.services.indicators_service import get_indicators
from app.services import bot_service
from app.dataclass.stock_dataclass import StockAnalyse, StockIndicators


def get_stock_analysis(ticker):
    logging.info(f'started {ticker}')

    stock = get_indicators(ticker, get_end_trading_day())

    logging.info(f'finished {ticker}')

    return stock


def analyze(request: StockAnalyse):
    logging.info(f'started {request}')

    stock = get_indicators(request.ticker, get_end_trading_day())

    if request.send_message:
        bot_service.send_stock_analyse(stock)

    logging.info(f'finished {request}')


def resume(tickers):
    logging.info(f'started ')
    stock_repository = ApplicationContext.instance().stock_repository

    date = get_end_trading_day()

    stocks = []
    for ticker in tickers:
        model = stock_repository.find_stock_by_ticker_and_date(
            ticker, str(date))
        if model:
            stocks.append(StockIndicators.from_model(model))

    bot_service.send_trend(stocks, str(date))

    logging.info(f'finished ')
