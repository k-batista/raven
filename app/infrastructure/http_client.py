import os

from dynaconf import settings
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def __no_proxies():
    return {'http': None, 'https': None}


def __get_proxies():
    return {
        'http': os.getenv('HTTP_PROXY', None),
        'https': os.getenv('HTTPS_PROXY', None)
    }


def retryable_client(
    retries=settings.HTTP.RETRIES,
    backoff_factor=settings.HTTP.BACKOFF_FACTOR,
    status_forcelist=settings.HTTP.RETRY_CODES,
    session=None,
):
    session = session or requests.Session()
    session.trust_env = False
    session.no_proxies = __no_proxies()
    session.proxies = __get_proxies()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
