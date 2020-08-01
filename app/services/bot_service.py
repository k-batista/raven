import logging

from app.clients import telegram_client as bot_client
from app.dataclass.stock_dataclass import StockIndicatorDataclass
from app.models.types import TimeFrame


def send_stock_analyse(dataclass: StockIndicatorDataclass, send=True):
    logging.info(f'started {dataclass.ticker}')

    message_html = dataclass.format_stock()

    if send:
        bot_client.send_message(message_html)
        return None
    else:
        logging.info(dataclass.ticker)
        return message_html


def send_setup(setups, time_frame, send=True, date=''):
    logging.info(f'started')

    if time_frame == TimeFrame.weekly.value:
        message_html = f'<b>SETUPS GRÁFICO SEMANAL</b> {date} \n'
    else:
        message_html = f'<b>SETUPS GRÁFICO DIÁRIO</b> {date} \n'

    for key, stocks in setups.items():

        message_html += f'<b>{key}</b> \U0001F535 \n'

        for ticker in stocks:
            message_html += f'{ticker}\n'

        message_html += '\n'

    if send:
        bot_client.send_message(message_html)
        return None
    else:
        print(message_html)
        return message_html
