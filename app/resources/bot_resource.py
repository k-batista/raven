import gevent

from dynaconf import settings
from flask import Blueprint, request
import telebot

from app.services import stock_service
from app.models.types import TimeFrame
from app.dataclass.stock_dataclass import StockAnalyseDataclass
from app.utils.constants import QuoteClient
from app.clients import count_client

TOKEN = settings.TELEGRAM.TOKEN
bot = telebot.TeleBot(TOKEN)
bp = Blueprint('bot', __name__)


menu = ("💎 /setups - Exibe todos os possíveis setups armados\n"
        "📊 /stocks - Exibe os indicadores diários da ação. "
        "Ex: /stocks BBDC4 \n")


@bot.message_handler(commands=['start', 'START'])
def start(message):
    bot.reply_to(
        message,
        f'Olá {message.from_user.first_name}, como posso te ajudar?\n'
        f'{menu}'
        "Meu canal: https://t.me/ravenspalerts ")


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(
        message.chat.id, menu)


@bot.message_handler(commands=['stocks', 'STOCKS'])
def stocks(message):
    gevent.spawn(count_client.count_stocks)
    ticker = get_ticker('/STOCKS', message)

    if ticker:
        analyse(message)
    else:
        sent = bot.send_message(message.chat.id,
                                "🔍 Envia a ação. Exemplo:  BBDC4  ou  VVAR3")
        bot.register_next_step_handler(sent, analyse)


def get_ticker(function, message):
    return message.text.upper().replace(function, '').replace(" ", "")


def analyse(message):
    ticker = get_ticker('/STOCKS', message)
    if not ticker or len(ticker) < 3:
        gevent.spawn(count_client.count_errors)
        bot.send_message(message.chat.id, "Ação não encontrada")
        return
    stock = StockAnalyseDataclass.build(
        ticker,
        TimeFrame.daily.value,
        False,
        QuoteClient.yahoo.value)
    bot.send_message(
        message.chat.id,
        stock_service.analyze(stock),
        parse_mode='HTML')


@bot.message_handler(commands=['analyze'])
def analyse_client(message):
    stock = StockAnalyseDataclass.build(
        get_ticker(
            '/ANALYZE',
            message),
        TimeFrame.daily.value,
        False,
        QuoteClient.alpha.value)
    bot.send_message(
        message.chat.id,
        stock_service.analyze(stock),
        parse_mode='HTML')


@bot.message_handler(commands=['setups', 'SETUPS'])
def setups(message):
    gevent.spawn(count_client.count_setups)
    bot.send_message(
        message.chat.id,
        stock_service.search_setups(TimeFrame.daily.value, False),
        parse_mode='HTML')


@bot.message_handler(commands=['setups_weekly'])
def setups_weekly(message):
    gevent.spawn(count_client.count_setups)
    bot.send_message(
        message.chat.id,
        stock_service.search_setups(TimeFrame.weekly.value, False),
        parse_mode='HTML')


@bot.message_handler(commands=['metrics'])
def metrics(message):
    bot.send_message(
        message.chat.id,
        count_client.metrics())


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(
        message,
        'Não entendi o que você quis dizer, use o /help para te ajudar')


@bp.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
