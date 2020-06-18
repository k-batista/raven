import logging

from app.clients import telegram_client as bot_client


def send_stock_analyse(stock):
    logging.info(f'started {stock.ticker}')

    trend_str = ''
    count_trend = stock.trend()

    if count_trend == 1:
        trend_str += (f'\n* <b>Tendência: Alta</b> ' + u"\U0001F535")
    elif count_trend == -1:
        trend_str += (f'\n* <b>Tendência: Baixa</b> ' + u"\U0001F534")
    else:
        trend_str += ('\n* <b>Tendência: Indefinida</b> ')

    # message_html = (f'<b>{stock.ticker}</b> - {stock.date} '
    #                 f'{stock.get_emoji()} [{stock.variation} %]\n'
    #                 f'<b>Preço</b> = Abr: {stock.price_open}'
    #                 f' Fch: {stock.price_close} \n'
    #                 f'VWAP diária = {stock.vwap()}\n'
    #                 f'EMA 9 = {stock.ema_9()}\n'
    #                 f'EMA 21 = {stock.ema_21()}\n'
    #                 # 'Média Exponencial 80 = {6}\n'
    #                 f'SMA 200 = {stock.sma_200()}'
    #                 # f'<b>Análise:</b> {analise}'
    #                 f'{trend_str}')
    
    message_html = format_stock(stock) + trend_str

    # print(message_html)
    bot_client.send_message(message_html)


def send_trend(stocks, date):
    logging.info(f'started')

    upward_trend = ''
    downtrend = ''
    undefined_trend = ''

    for stock in stocks:
        count_trend = stock.trend()

        if count_trend == 1:
            upward_trend += format_stock(stock, '+')
        elif count_trend == -1:
            downtrend += format_stock(stock, '-')
        else:
            undefined_trend += format_stock(stock, '~')
                # f'\n ~ {stock.ticker}  R$ {stock.price_close} [{stock.variation}]')
    
    trend_up = (f'<b>Resumo</b> - {date}'
                    f'\n* <b>Tendência: Alta</b> ' + u"\U0001F535 \n"
                    f'{upward_trend}')
    trend_down = (f'<b>Resumo</b> - {date}'
                f'\n* <b>Tendência: Baixa</b> ' + u"\U0001F534 \n"
                    f'{downtrend}')
    trend_undefined = (f'<b>Resumo</b> - {date}'
                    f'\n* <b>Tendência: Indefinida</b> \n'
                    f'{undefined_trend}')

    # # print(message_html)
    # bot_client.send_message(trend_up)
    # bot_client.send_message(trend_down)
    # bot_client.send_message(trend_undefined)

def format_stock(stock):
    return ('<b> {0:6}</b> - {13} {4}\n '
            '<b> Preço </b> Abr: {1} Fch: {2} [{3}]\n'
            '{5} <b>EMA 9</b> = {6:6} '
            ' {7} <b>EMA 21</b> = {8:6} '
            ' {9} <b>VWAP</b> = {10:6} '
            ' {11} <b>SMA 200</b> = {12:6} '
                        .format(stock.ticker, 
                            stock.price_open,
                            stock.price_close,
                                stock.variation, 
                                stock.get_emoji(), 
                                stock.ema_9_emoji(),stock.ema_9(),
                                stock.ema_21_emoji(),stock.ema_21(),
                                stock.vwap_emoji(),stock.vwap(),
                                stock.sma_200_emoji(), stock.sma_200(),
                                stock.date))