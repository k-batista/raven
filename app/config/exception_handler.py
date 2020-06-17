import logging


class ConfigErrorHandler:

    def config(self, app):
        app.register_error_handler(Exception, exception_handler)
        app.register_error_handler(ClientException, client_error_handler)
        app.register_error_handler(BusinessException, business_handler)


class ClientException(Exception):
    def __init__(self,
                 message,
                 customer_id=None,
                 level=logging.WARNING,
                 status_code=None,
                 event_state=None,
                 response_text=None):
        self.message = message
        self.customer_id = customer_id
        self.level = level
        self.status_code = status_code
        self.event_state = event_state
        self.response_text = response_text

    def get_message(self):
        return "message=%s customerId=%s" % (self.message, self.customer_id)


class NotFoundException(ClientException):
    pass


class BadRequestException(ClientException):
    pass


def client_error_handler(error):
    logging.log(error.level, error.get_message())

    return ({"message": error.get_message()},
            error.status_code,
            {'Content-Type': 'application/json'})


def exception_handler(error):
    logging.exception(error)

    return ({},
            500, {'Content-Type': 'application/json'})


def business_handler(message):
    logging.info(message)

    return ({"message": message.get_message()},
            200,
            {'Content-Type': 'application/json'})


class BusinessException(Exception):
    def __init__(self,
                 message):
        self.message = message
        self.status_code = 200

    def get_message(self):
        return self.message
