
from app.config.app_context import ApplicationContext
from app.clients import alphavantage_client as stock_client
from app.utils.business_days import get_business_day
from app.dataclass.stock_dataclass import StockIndicators
from app.models.stock import Stock


def get_indicators(ticker, date):
    stock_repository = ApplicationContext.instance().stock_repository

    stock = stock_repository.find_stock_by_ticker_and_date(ticker, str(date))

    if stock:
        return StockIndicators.from_model(stock)

    for days in range(9):
        today = get_business_day(get_business_day(date, -8), days)

        stock = stock_repository.find_stock_by_ticker_and_date(
            ticker, str(today))

        if not stock:
            dataclass = __get_indicators(ticker, today)
            stock = stock_repository.create(Stock.from_dataclass(dataclass))

    return StockIndicators.from_model(stock)


def __get_indicators(ticker, date):
    date_str = str(date)

    list_prices = __get_all_prices(ticker)

    price = list_prices.get(date_str)
    price_old = list_prices.get(str(get_business_day(date, -1)))

    vwap = __get_daily_vwap(ticker, date_str)
    ema_9 = __get_daily_ema(ticker, date_str, 9)
    ema_21 = __get_daily_ema(ticker, date_str, 21)
    sma_200 = __get_daily_sma(ticker, date_str, 200)

    stock = StockIndicators.build(ticker, price, date_str,
                                  price_old,
                                  {'vwap': vwap, 'ema_9': ema_9,
                                   'ema_21': ema_21, 'sma_200': sma_200})

    return stock


def __get_all_prices(ticker):
    response = stock_client.get_price(ticker, 'TIME_SERIES_DAILY')

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
