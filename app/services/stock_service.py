import logging

from app.config.app_context import ApplicationContext
from app.clients import alphavantage_client as stock_client
from app.clients import telegram_client as bot_client
from app.utils.business_days import get_end_trading_day, get_business_day
from app.dataclass.stock_dataclass import StockIndicators
from app.models.stock import Stock


def get_stock_analysis(ticker):

    logging.info(ticker)

    today = str(get_end_trading_day())

    return get_indicators(ticker, today)


def populate_database(ticker):
    logging.info(f'status=inital ticker={ticker}')
    stock_repository = ApplicationContext.instance().stock_repository

    for days in range(50):
        today = str(get_business_day(get_end_trading_day(), days * -1))

        stock = stock_repository.find_stock_by_ticker_and_date(ticker, today)

        if not stock:
            dataclass = get_indicators(ticker, today)
            stock_repository.create(Stock.from_dataclass(dataclass))

    send_message(ticker)
    logging.info(f'status=finished ticker={ticker}')


def send_message(ticker):
    logging.info(f'status=inital ticker={ticker}')
    stock_repository = ApplicationContext.instance().stock_repository

    today = str(get_end_trading_day())
    yesterday = str(get_business_day(get_end_trading_day(), -1))

    stock_today = stock_repository.find_stock_by_ticker_and_date(ticker, today)
    stock_yesterday = stock_repository.find_stock_by_ticker_and_date(
        ticker, yesterday)

    vwap = stock_today.indicators['vwap']
    ema_9 = stock_today.indicators['ema_9']
    ema_21 = stock_today.indicators['ema_21']
    sma_200 = stock_today.indicators['sma_200']

    analise = ''
    count_ta = 0
    count_tb = 0

    if ema_9 > ema_21:
        analise += ('\n + EMA 9 <b>acima</b> da EMA 21')
        count_ta += 1
    else:
        analise += ('\n - EMA 9 <b>abaixo</b> da EMA 21')
        count_tb += 1

    if stock_today.price_close >= ema_9:
        analise += ('\n + Fechamento diário <b>acima</b> da EMA 9 ')
        count_ta += 1
    else:
        analise += ('\n - Fechamento diário <b>abaixo</b> da EMA 9 ')
        count_tb += 1

    if stock_today.price_close >= ema_21:
        analise += ('\n + Fechamento diário <b>acima</b> da EMA 21 ')
        count_ta += 1
    else:
        analise += ('\n - Fechamento diário <b>abaixo</b> da EMA 21 ')
        count_tb += 1

    if stock_today.price_close >= vwap:
        analise += ('\n + Fechamento <b>acima</b> da VWAP ')
        count_ta += 1
    else:
        analise += ('\n - Fechamento <b>abaixo</b> da VWAP ')
        count_tb += 1

    down = u"\U0001F534"
    up = u"\U0001F535"

    if count_ta >= 3:
        analise += (f'\n* <b>Tendência: Alta</b> {up}')
    elif count_tb >= 3:
        analise += (f'\n* <b>Tendência: Baixa</b> {down}')
    else:
        analise += ('\n* <b>Tendência: Indefinida</b> ')

    emoji = stock_today.get_emoji(stock_yesterday)
    message_html = (f"<b>{ticker}</b> - {today} {emoji} [{stock_today.get_var(stock_yesterday)} %]\n"
                    f'<b>Preço</b> = Abr: {stock_today.price_open} Fch: {stock_today.price_close} \n'
                    f'VWAP diária = {vwap}\n'
                    f'EMA 9 = {ema_9}\n'
                    f'EMA 21 = {ema_21}\n'
                    # 'Média Exponencial 80 = {6}\n'
                    f'SMA 200 = {sma_200}\n'
                    f'<b>Análise:</b> {analise}')

    # print(message_html)
    bot_client.send_message(message_html)


def get_indicators(ticker, date):
    price = __get_daily_price(ticker, date)
    vwap = __get_daily_vwap(ticker, date)
    ema_9 = __get_daily_ema(ticker, date, 9)
    ema_21 = __get_daily_ema(ticker, date, 21)
    sma_200 = __get_daily_sma(ticker, date, 200)

    stock = StockIndicators.build(ticker, price, date,
                                  {'vwap': vwap, 'ema_9': ema_9,
                                   'ema_21': ema_21, 'sma_200': sma_200})

    return stock


def __get_daily_price(ticker, date):
    response = stock_client.get_price(ticker, 'TIME_SERIES_DAILY')

    return response.get(date)


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
