import logging

from app.clients import telegram_client as bot_client
from app.services.setup_service import find_setup


def send_stock_analyse(stock, send=True):
    logging.info(f'started {stock.ticker}')

    trend_str = ''
    count_trend = stock.trend()

    if count_trend == 1:
        trend_str += (f'\n* <b>Tendência: Alta</b> ' + u"\U0001F535")
    elif count_trend == -1:
        trend_str += (f'\n* <b>Tendência: Baixa</b> ' + u"\U0001F534")
    else:
        trend_str += ('\n* <b>Tendência: Indefinida</b> ')

    message_html = format_stock(stock) + trend_str

    if send:
        bot_client.send_message(message_html)
    else:
        print(message_html)
        print(find_setup(stock.ticker))


def send_setup(setups, send=True):
    logging.info(f'started')

    message_html = '<b>SETUPS GRÁFICO DIÁRIO</b> \n'
    for key, stocks in setups.items():

        message_html += f'<b>{key}</b> \U0001F535 \n'

        for ticker in stocks:
            message_html += f'{ticker}\n'

        message_html += '\n'

    if send:
        bot_client.send_message(message_html)
    else:
        print(message_html)


def format_stock(stock):
    return ('<b> {0:6}</b> - {13} '
            '\n<b> Preço </b> Abr: {1} Fch: {2} [{3} %]'
            '\n {5} <b>EMA 9</b> = {6:6} '
            '\n {7} <b>EMA 21</b> = {8:6} '
            '\n {9} <b>EMA 80</b> = {10:6} '
            '\n {11} <b>SMA 200</b> = {12:6} '
            .format(stock.ticker,
                    stock.price_open,
                    stock.price_close,
                    stock.variation,
                    stock.get_emoji(),
                    stock.ema_9_emoji(), stock.ema_9(),
                    stock.ema_21_emoji(), stock.ema_21(),
                    stock.ema_80_emoji(), stock.ema_80(),
                    stock.sma_200_emoji(), stock.sma_200(),
                    stock.date))
