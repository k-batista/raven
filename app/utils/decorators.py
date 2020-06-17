import logging

from app.config import exception_handler


# This one is intended to be used around functions that perform requests in
# external APIs using the http_caller.
def respond(factory):
    def decorator(fn):
        def decorated(*args, **kw):
            try:
                response = fn(*args, **kw)
            except exception_handler.ClientException as e:
                if e.status_code == 404:
                    raise exception_handler.NotFoundException(e.getMessage())

                logging.error(f"client error: {e.getMessage()}")
                raise

            if hasattr(factory, "from_json"):
                # This might raise if the data is not well-formed JSON.
                return factory.from_json(response)
            return factory

        decorated.__name__ = fn.__name__
        return decorated

    return decorator
