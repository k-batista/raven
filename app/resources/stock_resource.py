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

    return (
        stock.to_json(),
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/resume", methods=['POST'])
def resume():

    request_json = json.loads(request.data)

    stock_service.resume(request_json['stocks'])

    return ({}, StatusCode.OK.value, HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/analyze", methods=['POST'])
def analyze():

    request_json = json.loads(request.data)
    app = ApplicationContext.instance()

    for ticker in request_json['stocks']:
        stock = StockAnalyse.build(ticker, request_json['send_message'])
        app.queue.put(stock)

    return (
        {},
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/<ticker>/setup", methods=['GET'])
def setup(ticker):

    setup_service.find_setup(ticker)

    return ({},
            StatusCode.OK.value,
            HttpHeaders.JSON_HEADER.value)
