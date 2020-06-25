from dynaconf import settings
from flask import Blueprint, request
import telebot

from app.services import stock_service
from app.dataclass.stock_dataclass import StockAnalyse

TOKEN = settings.TELEGRAM.TOKEN
bot = telebot.TeleBot(TOKEN)
bp = Blueprint('bot', __name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        f'Olá {message.from_user.first_name}, como posso te ajudar?\n'
        "💎 /setups - envia os setups armados\n"
        "📊 /stocks - envia os valoreas de uma ação. Ex: /stocks BBDC4 \n"
        "Meu canal: https://t.me/ravenspalerts ")


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(
        message.chat.id,
        "💎 /setups - envia os setups armados\n"
        "📊 /stocks - envia os valoreas de uma ação\n"
        "Meu canal: https://t.me/ravenspalerts ")


@bot.message_handler(commands=['stocks', 'STOCKS'])
def stocks(message):
    ticker = message.text.upper().replace('/STOCKS ', '').replace(" ", "")
    stock = StockAnalyse.build(ticker, False)
    bot.send_message(
        message.chat.id,
        stock_service.analyze(stock),
        parse_mode='HTML')
    print(message.from_user.username)


@bot.message_handler(commands=['setups'])
def setups(message):
    bot.send_message(message.chat.id, get_setups(), parse_mode='HTML')
    print(message.from_user.username)


def get_setups():
    tickers = ["ABEV3", "AMAR3", "AZUL4", "B3SA3", "BBAS3",
               "BBDC4", "BBSE3", "BIDI4", "BOVA11", "BEEF3",
               "BRFS3", "BRKM5", "BRML3", "CAML3", "CCRO3",
               "CIEL3", "CMIG4", "CNTO3", "COGN3", "CSAN3",
               "CSNA3", "CYRE3", "CVCB3", "ECOR3", "EGIE3",
               "ELET3", "EMBR3", "EQTL3", "EZTC3", "FLRY3",
               "GFSA3", "GNDI3", "GOLL4", "GUAR3", "GGBR4",
               "GOAU4", "HBOR3", "HYPE3", "IRBR3", "ITSA4",
               "ITUB4", "JBSS3", "JHSF3", "KLBN11", "LAME4",
               "LINX3", "LREN3", "MGLU3", "MEAL3", "MRFG3",
               "ODPV3", "PETR4", "QUAL3", "RADL3", "RAIL3",
               "RENT3", "RAPT4", "SANB11", "SAPR4", "SMLS3",
               "SBSP3", "SUZB3", "TAEE11", "TASA4", "TCSA3",
               "UGPA3", "USIM5", "VALE3", "VIVT4", "VVAR3",
               "WEGE3", "WIZS3", "YDUQ3"]

    return stock_service.setup(tickers, False)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, 'Não é um comando válido')


@bp.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
