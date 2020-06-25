from collections import OrderedDict

from app.config.app_context import ApplicationContext
from app.clients import alphavantage_client as stock_client
from app.utils.business_days import get_business_day
from app.models.stock import Stock
from app.dataclass.stock_dataclass import StockIndicators


def get_indicators(ticker, date):
    stock_repository = ApplicationContext.instance().stock_repository

    stock = stock_repository.find_stock_by_ticker_and_date(ticker, str(date))

    if stock:
        return StockIndicators.from_model(stock)

    yesterday = get_business_day(date, -1)
    stock_yesterday = stock_repository.find_stock_by_ticker_and_date(
        ticker, str(yesterday))

    if stock_yesterday:
        stock = __create_history_indicators(ticker, date, stock_yesterday)
    else:
        stock = __create_history_indicators(ticker, date)

    return StockIndicators.from_model(stock)


def __update_indicators(ticker, date):
    stock_repository = ApplicationContext.instance().stock_repository

    prices = __get_all_prices(ticker, full=False)

    dataclass = __get_indicators(ticker, date, prices)
    stock = stock_repository.create(Stock.from_dataclass(dataclass))

    return stock


def __create_history_indicators(ticker, date, stock_yesterday=None):
    stock_repository = ApplicationContext.instance().stock_repository

    stock = None

    prices = __get_all_prices(ticker, True)

    for days in range(9):
        today = get_business_day(get_business_day(date, -8), days)

        stock = stock_repository.find_stock_by_ticker_and_date(
            ticker, str(today))

        if not stock:
            dataclass = __get_indicators(
                ticker, today, prices, stock_yesterday)
            stock = stock_repository.create(Stock.from_dataclass(dataclass))

    return stock


def __get_indicators(ticker, date, prices, stock_yesterday=None):
    date_str = str(date)

    # Prices
    all_prices = OrderedDict(sorted(prices.items()))
    reverse_prices = OrderedDict(sorted(prices.items(), reverse=True))

    if stock_yesterday:
        price_old = float(stock_yesterday.price_close)
    else:
        price_old = __get_price(all_prices.get(
            str(get_business_day(date, -1))))

    price = all_prices.get(date_str)

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


def __get_price(stock):
    return float(stock.get('4. close'))


def __get_price_by_date(prices, date):
    price = prices.get(date)

    if price:
        return float(price.get('4. close'))

    return None


def get_var(price, price_old):
    return round(
        (((__get_price(price) * 100) / price_old) - 100), 2)


def ema(period, prices):

    emas = {}
    count = 1
    average = 0
    multiplier = 2 / (period + 1)

    for key, values in prices:

        value = __get_price(values)

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

    for key, values in prices:
        if count == period:
            break

        if key == str(date) or count > 0:
            count += 1
            average += __get_price(values)
            # print(str(average) + '- '+(str(date)))

    return round(average / period, 2)


def __get_all_prices(ticker, full=False):
    response = stock_client.get_price(ticker, 'TIME_SERIES_DAILY', full)

    return response


def __get_daily_ema(ticker, date, period):
    response = stock_client.get_ema(ticker, 'daily', period)

    return round(float(response.get(date)['EMA']), 2)


def __get_daily_sma(ticker, date, period):
    response = stock_client.get_sma(ticker, 'daily', period)

    return round(float(response.get(date)['SMA']), 2)


def __get_daily_vwap(ticker, date):
    response = stock_client.get_vwap(ticker)

    average_vwap = 0
    count = 6

    hour_trading_floor = 10
    for hour in range(6):
        vwap = response.get(f'{date} {hour_trading_floor + hour}:00')
        if not vwap:
            count = count - 1
            continue

        average_vwap += float(vwap['VWAP'])

    return round(average_vwap / count, 2)
