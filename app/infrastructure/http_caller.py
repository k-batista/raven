import logging
import json

from requests.exceptions import RequestException

from .http_client import retryable_client
from app.config.exception_handler import ClientException

http_client = retryable_client()
__http_proxies = http_client.proxies
__no_http_proxies = http_client.no_proxies
__default_timeout = 2


def get(
        url,
        timeout=None,
        headers=None,
        params=None,
        use_proxy=False,
        return_status_http=False,
        parse_json=False):
    call_timeout = timeout if timeout is not None else __default_timeout
    proxies = __no_http_proxies if not use_proxy else __http_proxies
    try:
        response = http_client.get(url, timeout=call_timeout,
                                   params=params,
                                   proxies=proxies, headers=headers)

        return __check_response_before_return(response, return_status_http,
                                              parse_json)
    except RequestException as exc:
        logging.error(exc)
        raise exc


def put(
        url,
        timeout=None,
        data=None,
        headers=None,
        use_proxy=False,
        return_status_http=False,
        parse_json=False):
    call_timeout = timeout if timeout is not None else __default_timeout
    proxies = __no_http_proxies if not use_proxy else __http_proxies
    try:
        response = http_client.put(url, timeout=call_timeout, data=data,
                                   headers=headers, proxies=proxies)

        return __check_response_before_return(response, return_status_http,
                                              parse_json)
    except RequestException as exc:
        logging.error(exc)
        raise exc


def post(
        url,
        timeout=None,
        data=None,
        headers=None,
        use_proxy=False,
        return_status_http=False,
        parse_json=False):
    call_timeout = timeout if timeout is not None else __default_timeout
    proxies = __no_http_proxies if not use_proxy else __http_proxies
    try:
        response = http_client.post(url,
                                    timeout=call_timeout,
                                    data=data,
                                    headers=headers,
                                    proxies=proxies)

        return __check_response_before_return(response, return_status_http,
                                              parse_json)
    except RequestException as exc:
        logging.error(exc)
        raise exc


def patch(
        url,
        timeout=None,
        data=None,
        headers=None,
        use_proxy=False,
        return_status_http=False,
        parse_json=False):
    call_timeout = timeout if timeout is not None else __default_timeout
    proxies = __no_http_proxies if not use_proxy else __http_proxies
    try:
        response = http_client.patch(url,
                                     timeout=call_timeout,
                                     data=data,
                                     headers=headers,
                                     proxies=proxies)

        return __check_response_before_return(response, return_status_http,
                                              parse_json)
    except RequestException as exc:
        logging.error(exc)
        raise exc


def __check_response_before_return(
        response,
        return_status_http=False,
        parse_json=False):
    status_code = response.status_code

    if status_code >= 500:
        raise Exception(f'Error in URL: {response.url} '
                        f'status={status_code} response={response.text}')

    elif status_code >= 400:
        raise ClientException(
            message=f'Error in URL: {response.url} status={status_code} '
                    f'response={response.text}',
            status_code=status_code,
            response_text=response.text
        )

    if return_status_http:
        return response
    else:
        if parse_json:
            return json.loads(response.text)

        return response.text
