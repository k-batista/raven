import logging


from app.infrastructure import http_caller
from app.config.exception_handler import ClientException


def health():
    try:
        return http_caller.get(url='http://ravensp.herokuapp.com/health',
                               timeout=10)

    except ClientException as exc:
        logging.exception(exc)
        raise exc
