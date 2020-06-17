from enum import Enum


class HttpHeaders(Enum):
    JSON_HEADER = {'Content-Type': 'application/json'}


class StatusCode(Enum):
    OK = 200
    CREATED = 201
    PARTIAL_CONTENT = 206
