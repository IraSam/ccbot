import datetime as dt
import functools
import logging
import os
import sys
import tempfile


def logging_inputs_info(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'calling {func.__name__} with arguments {args} and keyword arguments {kwargs}')
        return func(*args, **kwargs)

    return wrapper


def setup_logging(log_level: logging = logging.INFO, dest_file: str = None) -> None:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    root = logging.getLogger()
    root.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    if dest_file:
        file_handler = logging.FileHandler(dest_file, mode='w')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)


def create_log_filename(suffix: str) -> str:
    return os.path.join(tempfile.gettempdir(), 'crypto', f'{dt.datetime.now().strftime("%Y%m%d_%H%M%S")}_{suffix}.txt')
