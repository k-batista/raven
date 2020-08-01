import logging

from dynaconf import settings
from expiringdict import ExpiringDict

from app.infrastructure import http_caller
from app.config.exception_handler import ClientException
from app.dataclass.quote_dataclass import QuoteDataclass


base_url = settings.ALPHAVANTAGE.URL
token = settings.ALPHAVANTAGE.TOKEN
timeout = settings.ALPHAVANTAGE.TIMEOUT

cache = ExpiringDict(max_len=100, max_age_seconds=300)


def get_prices(request, date, full):

    time_series = 'TIME_SERIES_DAILY'
    selector = 'Time Series (Daily)'
    if request.time_frame == 'weekly':
        time_series = 'TIME_SERIES_WEEKLY'
        selector = 'Weekly Time Series'

    url = (
        base_url +
        f'?function={time_series}&symbol={request.ticker}.SAO&apikey={token}')

    if full:
        url += '&outputsize=full'

    try:
        key = f'{request.ticker}_price'
        response_cache = cache.get(key)
        if response_cache:
            return response_cache

        response = (http_caller.get(url=url, timeout=timeout, parse_json=True)
                    [selector])

        quotes = dict()

        for date, stock in response.items():
            quote = QuoteDataclass.from_alphavantage(
                request.ticker, stock, date)
            if quote:
                quotes[quote.date] = quote

        cache[key] = quotes
        return quotes

    except ClientException as exc:
        logging.error('Erro ao realizar consulta')
        raise exc
