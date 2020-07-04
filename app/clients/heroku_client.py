import logging

from dynaconf import settings

from app.infrastructure import http_caller
from app.config.exception_handler import ClientException


base_url = settings.HEROKU.URL
timeout = settings.HEROKU.TIMEOUT


def health():
    try:
        return http_caller.get(url=f'{base_url}health', timeout=timeout)
    except ClientException as exc:
        logging.exception(exc)
        raise exc
