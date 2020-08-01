from datetime import datetime


from app.config.app_context import ApplicationContext
from app.utils.business_days import get_business_day
from app.models.stock import Stock
from app.dataclass.stock_dataclass import StockIndicatorDataclass
from app.services.indicators import StockIndicator


def generate_stock_indicators(request, date):
    stock_repository = ApplicationContext.instance().stock_repository

    stock = stock_repository.find_stock_by_ticker_and_timeframe_and_date(
        request.ticker, request.time_frame, str(date))

    if stock:
        return StockIndicatorDataclass.from_model(stock)

    indicator = StockIndicator(request, date)
    stock = (__create_stock_daily(request, date, indicator)
             if request.time_frame == 'daily'
             else __create_stock_weekly(request, indicator))

    return StockIndicatorDataclass.from_model(stock)


def __create_stock_weekly(request, indicator):
    stock_repository = ApplicationContext.instance().stock_repository
    count = 0
    for key, value in indicator.reverse_prices.items():
        if count == 7:
            break

        count += 1

        stock = stock_repository.find_stock_by_ticker_and_timeframe_and_date(
            request.ticker, request.time_frame, key)

        if not stock:
            dataclass = __create_stock(
                request, datetime.strptime(
                    key, '%Y-%m-%d').date(), indicator)
            stock = stock_repository.create(Stock.from_dataclass(dataclass))

    return stock


def __create_stock_daily(request, date, indicator):
    stock_repository = ApplicationContext.instance().stock_repository

    for days in range(9):
        today = get_business_day(get_business_day(date, -8), days)
        stock = stock_repository.find_stock_by_ticker_and_timeframe_and_date(
            request.ticker, request.time_frame, str(today))

        if not stock:
            dataclass = __create_stock(request, today, indicator)
            stock = stock_repository.create(Stock.from_dataclass(dataclass))

    return stock


def __create_stock(request, date, indicator):
    date_str = str(date)
    price = indicator.get_price_by_date(date_str)
    price_old = __get_price_old(indicator, request, date)

    return StockIndicatorDataclass.build(
        request, price, date_str, __get_variation(
            price, price_old), {
            'ema_9': indicator.get_ema(
                9, date_str), 'ema_21': indicator.get_ema(
                    21, date_str), 'ema_80': indicator.get_ema(
                        80, date_str), 'sma_9': indicator.get_sma(
                            9, date_str), 'sma_200': indicator.get_sma(
                                200, date_str)})


def __get_price_old(indicator, request, date):
    stock_repository = ApplicationContext.instance().stock_repository

    yesterday = str(get_business_day(date, -1))

    stock = stock_repository.find_stock_by_ticker_and_timeframe_and_date(
        request.ticker, request.time_frame, yesterday)

    if stock:
        return float(stock.price_close())

    if request.time_frame == 'weekly':
        end_week = get_business_day(date, -1)

        for day in range(5):
            end_week = get_business_day(end_week, -1)
            stock = indicator.get_price_by_date(str(end_week))

            if stock:
                break

        return stock

    return indicator.get_price_by_date(yesterday)


def __get_variation(current, old):
    return round(
        (((current.price_close * 100) / old.price_close) - 100), 2)
