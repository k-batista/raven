import logging

from app.config.app_context import ApplicationContext
from app.services.indicators_service import get_indicators
from app.services.setup_service import find_setup
from app.services import bot_service
from app.dataclass.stock_dataclass import StockIndicators, StockAnalyse
from app.utils.business_days import get_end_trading_day


def get_stock_analysis(ticker):
    try:
        logging.info(f'started {ticker}')

        app = ApplicationContext.instance()
        stock_repository = app.stock_repository

        today = str(get_end_trading_day())

        stock = stock_repository.find_stock_by_ticker_and_date(ticker, today)

        if stock:
            return StockIndicators.from_model(stock)
        else:
            stock = StockAnalyse.build(ticker, False)
            app.queue.put(stock)
            return None
    finally:
        logging.info(f'finished {ticker}')


def analyze(request: StockAnalyse):
    logging.info(f'started {request}')
    try:
        stock = get_indicators(request.ticker, get_end_trading_day())

        return bot_service.send_stock_analyse(stock, request.send_message)
    except Exception as ex:
        logging.exception(ex)
        return 'Tente novamente, aconteceu um problema'
    finally:
        logging.info(f'finished {request}')


def setup(tickers, send_message):
    logging.info(f'started ')

    try:
        setups = dict()
        for ticker in tickers:
            setup = find_setup(ticker)

            if setup:
                stocks = setups.get(setup)

                if not stocks:
                    stocks = []

                stocks.append(ticker)
                setups[setup] = stocks

        print(setups)

        return bot_service.send_setup(setups, send_message)
    except Exception as ex:
        logging.exception(ex)
        return 'Tente novamente, aconteceu um problema'
    finally:
        logging.info(f'finished ')
