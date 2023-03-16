import functools
import logging


def logging_inputs_info(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'calling {func.__name__} with arguments {args} and keyword arguments {kwargs}')
        return func(*args, **kwargs)

    return wrapper
