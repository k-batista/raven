import logging

from app.utils.business_days import get_end_trading_day
from app.services.indicators_service import get_indicators
from app.services.setup_service import find_setup
from app.services import bot_service
from app.dataclass.stock_dataclass import StockAnalyse


def get_stock_analysis(ticker):
    logging.info(f'started {ticker}')

    stock = get_indicators(ticker, get_end_trading_day())

    logging.info(f'finished {ticker}')

    return stock


def analyze(request: StockAnalyse):
    logging.info(f'started {request}')

    stock = get_indicators(request.ticker, get_end_trading_day())

    bot_service.send_stock_analyse(stock, request.send_message)

    logging.info(f'finished {request}')


def setup(tickers, send_message):
    logging.info(f'started ')

    setups = dict()
    for ticker in tickers:
        setup = find_setup(ticker)

        if setup:
            stocks = setups.get(setup)

            if not stocks:
                stocks = []

            stocks.append(ticker)
            setups[setup] = stocks

    bot_service.send_setup(setups, send_message)

    logging.info(f'finished ')
