from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class QuoteClient(AutoName):
    yahoo = auto()
    alpha = auto()


class HttpHeaders(Enum):
    JSON_HEADER = {'Content-Type': 'application/json'}


class StatusCode(Enum):
    OK = 200
    CREATED = 201
    PARTIAL_CONTENT = 206
