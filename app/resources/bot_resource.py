from dynaconf import settings
from flask import Blueprint, request
import telebot

from app.services import stock_service
from app.dataclass.stock_dataclass import StockAnalyse

TOKEN = settings.TELEGRAM.TOKEN
bot = telebot.TeleBot(TOKEN)
bp = Blueprint('bot', __name__)


menu = ("💎 /setups - Exibe todos os possíveis setups armados\n"
        "📊 /stocks - Exibe os indicadores diários da ação. "
        "Ex: /stocks BBDC4 \n")


@bot.message_handler(commands=['start'])
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
    ticker = get_ticker(message)

    if ticker:
        analyse(message)
    else:
        sent = bot.send_message(message.chat.id,
                                "🔍 Envia a ação. Exemplo:  BBDC4  ou  VVAR3")
        bot.register_next_step_handler(sent, analyse)


def get_ticker(message):
    return message.text.upper().replace('/STOCKS', '').replace(" ", "")


def analyse(message):
    ticker = get_ticker(message)
    if not ticker or len(ticker) < 3:
        bot.send_message(message.chat.id, "Ação não encontrada")
        return
    stock = StockAnalyse.build(ticker, False)
    bot.send_message(
        message.chat.id,
        stock_service.analyze(stock),
        parse_mode='HTML')


@bot.message_handler(commands=['setups'])
def setups(message):
    bot.send_message(
        message.chat.id,
        stock_service.search_setups(False),
        parse_mode='HTML')


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
