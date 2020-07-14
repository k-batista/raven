import json
from flask import Blueprint, request

from app.utils.constants import StatusCode, HttpHeaders
from app.services import stock_service
from app.config.app_context import ApplicationContext
from app.models.stock import Stock
from app.dataclass.stock_dataclass import StockAnalyse
from app.dataclass.stock_dataclass import StockIndicators
from app.dataclass.stock_dataclass import StockIndicatorsList


bp = Blueprint('stocks', __name__)


@bp.route("/stocks/<ticker>", methods=['GET'])
def get_stock(ticker):

    app = ApplicationContext.instance()
    stock_repository = app.stock_repository

    stocks = StockIndicatorsList.build(
        stock_repository.find_all_stocks_by_ticker(ticker))

    return (stocks.to_json(),
            StatusCode.OK.value,
            HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/<ticker>", methods=['POST'])
def create_stock(ticker):

    app = ApplicationContext.instance()
    stock_repository = app.stock_repository

    stock = Stock.from_dataclass(
        StockIndicators.from_json(request.data))

    stock_repository.create(stock)

    return ({},
            StatusCode.CREATED.value,
            HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/<ticker>/analyse", methods=['GET'])
def analyse_stock(ticker):

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

    stock_service.search_setups(request_json['send_message'])

    return ({}, StatusCode.OK.value, HttpHeaders.JSON_HEADER.value)
