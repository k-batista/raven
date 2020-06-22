import json
from flask import Blueprint, request

from app.utils.constants import StatusCode, HttpHeaders
from app.services import stock_service
from app.services import setup_service
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


@bp.route("/stocks/setup", methods=['POST'])
def setups():

    request_json = json.loads(request.data)

    stock_service.setup(request_json['stocks'], request_json['send_message'])

    return ({}, StatusCode.OK.value, HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/<ticker>/setup", methods=['GET'])
def setup(ticker):

    setup_service.find_setup(ticker)

    return ({},
            StatusCode.OK.value,
            HttpHeaders.JSON_HEADER.value)
