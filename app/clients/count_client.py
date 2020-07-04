import logging

from dynaconf import settings

from app.infrastructure import http_caller
from app.config.exception_handler import ClientException

base_url = settings.COUNT.URL
timeout = settings.COUNT.TIMEOUT


def count_stocks():
    try:
        return http_caller.get(url=f'{base_url}hit/ravensp_stocks',
                               timeout=timeout)
    except ClientException as exc:
        logging.exception(exc)


def count_setups():
    try:
        return http_caller.get(url=f'{base_url}hit/ravensp_setups',
                               timeout=timeout)
    except ClientException as exc:
        logging.exception(exc)


def count_errors():
    try:
        return http_caller.get(url=f'{base_url}hit/ravensp_errors',
                               timeout=timeout)
    except ClientException as exc:
        logging.exception(exc)


def metrics():
    try:
        stocks = http_caller.get(url=f'{base_url}get/ravensp_stocks',
                                 timeout=timeout, parse_json=True)
        setups = http_caller.get(url=f'{base_url}get/ravensp_setups',
                                 timeout=timeout, parse_json=True)
        errors = http_caller.get(url=f'{base_url}get/ravensp_errors',
                                 timeout=timeout, parse_json=True)
        return (f'stocks: {stocks}\n'
                f'setups: {setups}\n'
                f'errors: {errors}')

    except ClientException as exc:
        logging.exception(exc)
