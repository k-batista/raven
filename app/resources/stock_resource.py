import json
from flask import Blueprint, request

from app.utils.constants import StatusCode, HttpHeaders
from app.services import stock_service
from app.config.app_context import ApplicationContext
from app.dataclass.stock_dataclass import StockAnalyse


bp = Blueprint('stocks', __name__)


@bp.route("/stocks/<ticker>", methods=['GET'])
def get_stock(ticker):

    stock = stock_service.get_stock_analysis(ticker)

    if not stock:
        return ({'message': 'Sua solicitação foi recebida e '
                 'adicionada na fila de processamento'},
                StatusCode.CREATED.value, HttpHeaders.JSON_HEADER.value)

    return (
        stock.to_json(),
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/analyze", methods=['POST'])
def analyze():

    request_json = json.loads(request.data)
    app = ApplicationContext.instance()

    for ticker in request_json['stocks']:
        stock = StockAnalyse.build(ticker, request_json['send_message'])
        app.put_queue(stock)

    return (
        {},
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/analyze", methods=['GET'])
def cron_analyze():

    app = ApplicationContext.instance()

    for ticker in ["ABEV3", "AMAR3", "AZUL4", "B3SA3", "BBAS3",
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
                   "WEGE3", "WIZS3", "YDUQ3"]:

        stock = StockAnalyse.build(ticker, False)
        app.put_queue(stock)

    return (
        {},
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/setup", methods=['GET'])
def cron_setup():

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

    stock_service.setup(tickers, True)

    return (
        {},
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/setup", methods=['POST'])
def setups():

    request_json = json.loads(request.data)

    stock_service.setup(request_json['stocks'], request_json['send_message'])

    return ({}, StatusCode.OK.value, HttpHeaders.JSON_HEADER.value)
