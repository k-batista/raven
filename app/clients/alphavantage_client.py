import logging

from dynaconf import settings
from expiringdict import ExpiringDict

from app.infrastructure import http_caller
from app.config.exception_handler import ClientException


base_url = settings.ALPHAVANTAGE.URL
token = settings.ALPHAVANTAGE.TOKEN
timeout = settings.ALPHAVANTAGE.TIMEOUT

cache = ExpiringDict(max_len=500, max_age_seconds=3600)


def get_price(ticker, time):
    url = (base_url + f'?function={time}&symbol={ticker}.SAO&apikey={token}')

    try:
        key = f'{ticker}_price'
        response_cache = cache.get(key)
        if response_cache:
            return response_cache

        response = (http_caller.get(url=url, timeout=timeout, parse_json=True)
                    ['Time Series (Daily)'])
        cache[key] = response

        return response

    except ClientException as exc:
        logging.error('Erro ao realizar consulta')
        raise exc


def get_ema(ticker, interval, period):
    url = (base_url +
           f'?function=EMA&symbol={ticker}.SAO&interval={interval}'
           f'&time_period={period}&series_type=close&apikey={token}')

    try:
        key = f'{ticker}_ema_{period}'

        response_cache = cache.get(key)
        if response_cache:
            return response_cache

        response = (http_caller.get(url=url, timeout=timeout, parse_json=True)
                    ['Technical Analysis: EMA'])
        cache[key] = response

        return response

    except ClientException as exc:
        logging.error('Erro ao realizar consulta')
        raise exc


def get_sma(ticker, interval, period):
    url = (base_url +
           f'?function=SMA&symbol={ticker}.SAO&interval={interval}'
           f'&time_period={period}&series_type=close&apikey={token}')

    try:
        key = f'{ticker}_sma_{period}'

        response_cache = cache.get(key)
        if response_cache:
            return response_cache

        response = (http_caller.get(url=url, timeout=timeout, parse_json=True)
                    ['Technical Analysis: SMA'])
        cache[key] = response

        return response

    except ClientException as exc:
        logging.error('Erro ao realizar consulta')
        raise exc


def get_vwap(ticker):
    url = (base_url +
           f'?function=VWAP&symbol={ticker}.SAO&interval=60min&apikey={token}')

    try:
        key = f'{ticker}_vwap'

        response_cache = cache.get(key)
        if response_cache:
            return response_cache

        response = (http_caller.get(url=url, timeout=timeout, parse_json=True)
                    ['Technical Analysis: VWAP'])
        cache[key] = response

        return response

    except ClientException as exc:
        logging.error('Erro ao realizar consulta')
        raise exc
