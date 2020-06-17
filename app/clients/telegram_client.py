import logging

from dynaconf import settings

from app.infrastructure import http_caller
from app.config.exception_handler import ClientException


base_url = settings.TELEGRAM.URL
token = settings.TELEGRAM.TOKEN
timeout = settings.TELEGRAM.TIMEOUT


def send_message(html):
    url = f'{base_url}/{token}/sendMessage'
    params = {'chat_id': '@ravenspalerts', 'parse_mode': 'html',
              'text': html}

    try:
        return http_caller.get(url=url, timeout=timeout, params=params)

    except ClientException as exc:
        logging.exception(exc)
        raise exc
