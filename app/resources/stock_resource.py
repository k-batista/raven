import json
from flask import Blueprint, request

from app.utils.constants import StatusCode, HttpHeaders
from app.services import stock_service
from app.config.app_context import ApplicationContext


bp = Blueprint('stock', __name__)


@bp.route("/stock/<ticker>", methods=['GET'])
def get_stock(ticker):

    stock = stock_service.get_stock_analysis(ticker)

    return (
        stock.to_json(),
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)


@bp.route("/populate_database", methods=['POST'])
def populate_database():

    request_json = json.loads(request.data)
    app = ApplicationContext.instance()

    for ticker in request_json['list']:
        app.queue.put(ticker)

    return (
        {},
        StatusCode.OK.value,
        HttpHeaders.JSON_HEADER.value)
