import logging
import sys
from logging.handlers import TimedRotatingFileHandler


def get_console_handler(formatter=False):
    console_handler = logging.StreamHandler(sys.stdout)
    if formatter:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - line %(lineno)s - %(message)s")
        console_handler.setFormatter(formatter)
    return console_handler


def get_file_handler(log_file, formatter=False):
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    if formatter:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - line %(lineno)s - %(message)s")
        file_handler.setFormatter(formatter)
    return file_handler


def get_logger(logger_name, log_file, use_formatter=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler(use_formatter))
    logger.addHandler(get_file_handler(log_file, use_formatter))
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
