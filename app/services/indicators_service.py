from collections import OrderedDict

from app.config.app_context import ApplicationContext
from app.clients import alphavantage_client
from app.clients import yahoo_client
from app.utils.business_days import get_business_day
from app.models.stock import Stock
from app.dataclass.stock_dataclass import StockIndicators


def get_indicators(ticker, date):
    stock_repository = ApplicationContext.instance().stock_repository

    stock = stock_repository.find_stock_by_ticker_and_date(ticker, str(date))

    if stock:
        return StockIndicators.from_model(stock)

    stock = __create_history_indicators(ticker, date)

    return StockIndicators.from_model(stock)


def __create_history_indicators(ticker, date):
    stock_repository = ApplicationContext.instance().stock_repository

    stock = None

    prices = __get_all_prices(ticker, date)

    for days in range(9):
        today = get_business_day(get_business_day(date, -8), days)

        stock = stock_repository.find_stock_by_ticker_and_date(
            ticker, str(today))

        if not stock:
            dataclass = __get_indicators(ticker, today, prices)
            stock = stock_repository.create(Stock.from_dataclass(dataclass))

    return stock


def __get_indicators(ticker, date, prices):
    date_str = str(date)

    # Prices
    all_prices = OrderedDict(sorted(prices.items()))
    reverse_prices = OrderedDict(sorted(prices.items(), reverse=True))

    price = all_prices.get(date_str)
    price_old = all_prices.get(str(get_business_day(date, -1)))

    # Indicators
    variation = get_var(price, price_old)
    ema_9 = ema(9, all_prices.items()).get(date_str)
    ema_21 = ema(21, all_prices.items()).get(date_str)
    ema_80 = ema(80, all_prices.items()).get(date_str)
    sma_9 = sma(9, reverse_prices.items(), date)
    sma_200 = sma(200, reverse_prices.items(), date)

    stock = StockIndicators.build(ticker, price, date_str,
                                  variation,
                                  {'ema_9': ema_9,
                                   'ema_21': ema_21, 'ema_80': ema_80,
                                   'sma_9': sma_9, 'sma_200': sma_200})

    return stock


def get_var(price, price_old):
    return round(
        (((price.price_close * 100) / price_old.price_close) - 100), 2)


def ema(period, prices):

    emas = {}
    count = 1
    average = 0
    multiplier = 2 / (period + 1)

    for key, stock in prices:

        value = stock.price_close

        if count < period:
            average += value
            count += 1
            continue
        elif count == period:
            average = average / (period - 1)
            count += 1

        ema = round((((value - average) * multiplier) + average), 2)
        emas[key] = ema
        average = ema

    return emas


def sma(period, prices, date):

    count = 0
    average = 0

    for key, stock in prices:
        if count == period:
            break

        if key == str(date) or count > 0:
            count += 1
            average += stock.price_close

    return round(average / period, 2)


def __get_all_prices(ticker, date, full=True):
    if True:
        return yahoo_client.get_prices(ticker, date, full)
    else:
        return alphavantage_client.get_prices(ticker, full)
