import logging

from dynaconf import settings
from expiringdict import ExpiringDict

from app.infrastructure import http_caller
from app.utils.business_days import get_business_day, get_timestamp
from app.config.exception_handler import ClientException
from app.dataclass.quote_dataclass import QuoteDataclass


base_url = settings.YAHOO.URL
timeout = settings.YAHOO.TIMEOUT

cache = ExpiringDict(max_len=100, max_age_seconds=300)


def get_prices(request, date, full):

    timestamp = get_timestamp(date)
    old_timestamp = -2208988800

    if not full:
        old_timestamp = get_timestamp(get_business_day(date, -10))

    url = (
        f'{base_url}v8/finance/chart/{request.ticker}.SA?'
        f'period1={old_timestamp}&period2={timestamp}&interval=1d')

    try:
        key = f'{request.ticker}_price'
        response_cache = cache.get(key)
        if response_cache:
            return response_cache

        response = (http_caller.get(url=url, timeout=timeout, parse_json=True)
                    ['chart']['result'][0])
        response_quotes = response['indicators']['quote'][0]
        quotes = dict()

        for index, value in enumerate(response['timestamp']):
            quote = QuoteDataclass.from_yahoo(
                request.ticker, response_quotes, index, value)
            if quote:
                quotes[quote.date] = quote

        cache[key] = quotes
        return quotes

    except ClientException as exc:
        logging.error('Erro ao realizar consulta')
        raise exc
