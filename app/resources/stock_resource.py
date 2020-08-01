import json
from flask import Blueprint, request

from app.utils.constants import StatusCode, HttpHeaders
from app.services import stock_service
from app.config.app_context import ApplicationContext
from app.models.stock import Stock
from app.models.types import TimeFrame
from app.utils.business_days import get_end_trading_day
from app.dataclass import stock_dataclass as stock_dc
from app.services.indicators import StockIndicator


bp = Blueprint('stocks', __name__)


@bp.route("/stocks/<ticker>", methods=['GET'])
def resource_get_stock(ticker):
    time_frame = extract_time_frame(request.args.get('time_frame'))

    stock_repository = (ApplicationContext.instance()
                        .stock_repository)

    stocks = stock_dc.StockIndicatorListDataclass.build(
        stock_repository.find_all_stocks_by_ticker(ticker, time_frame))

    return (stocks.to_json(),
            StatusCode.OK.value,
            HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/<ticker>", methods=['POST'])
def resource_create_stock(ticker):

    stock_repository = (ApplicationContext.instance()
                        .stock_repository)

    stock = Stock.from_dataclass(
        stock_dc.StockIndicatorDataclass.from_json(request.data))

    stock_repository.create(stock)

    return ({},
            StatusCode.CREATED.value,
            HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/<ticker>/analyze", methods=['GET'])
def resource_analyse_stock(ticker):
    time_frame = extract_time_frame(request.args.get('time_frame'))

    stock = stock_service.get_stock_analysis(ticker, time_frame)

    if not stock:
        return ({'message': 'Sua solicitação foi recebida e '
                 'adicionada na fila de processamento'},
                StatusCode.CREATED.value, HttpHeaders.JSON_HEADER.value)

    return (
        stock.to_json(),
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/analyze", methods=['POST'])
def resource_analyze():
    request_json = json.loads(request.data)
    app = ApplicationContext.instance()

    time_frame = extract_time_frame(request_json['time_frame'])

    for ticker in request_json['stocks']:
        stock = stock_dc.StockAnalyseDataclass.build(
            ticker,
            time_frame,
            request_json['send_message'],
            'alpha')
        app.put_queue(stock)

    return (
        {},
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)


@bp.route("/stocks/setup", methods=['POST'])
def resource_setups():
    request_json = json.loads(request.data)
    time_frame = extract_time_frame(request_json['time_frame'])

    stock_service.search_setups(time_frame, request_json['send_message'])

    return ({}, StatusCode.OK.value, HttpHeaders.JSON_HEADER.value)


def extract_time_frame(time_frame):
    if not time_frame:
        return TimeFrame.daily.value

    if time_frame not in [TimeFrame.daily.value, TimeFrame.weekly.value]:
        return TimeFrame.daily.value

    return time_frame
