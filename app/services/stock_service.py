import logging

from app.config.app_context import ApplicationContext
from app.clients import telegram_client as bot_client
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
        bot_client.send_error(f' Ticker: {request.ticker}  ERRO: {repr(ex)}')
        return 'Tente novamente, aconteceu um problema'
    finally:
        logging.info(f'finished {request}')


def search_setups(send_message):
    logging.info(f'started ')

    stock_repository = ApplicationContext.instance().stock_repository

    try:
        setups = dict()
        today = str(get_end_trading_day())

        tickers = stock_repository.find_all_tickers()

        for ticker in tickers:
            setup = find_setup(ticker[0], today)

            if setup:
                stocks = setups.get(setup)

                if not stocks:
                    stocks = []

                stocks.append(ticker[0])
                setups[setup] = stocks

        return bot_service.send_setup(setups, send_message, today)
    except Exception as ex:
        logging.exception(ex)
        bot_client.send_error(f' Setup  ERRO: {repr(ex)}')
        return 'Tente novamente, aconteceu um problema'
    finally:
        logging.info(f'finished ')
