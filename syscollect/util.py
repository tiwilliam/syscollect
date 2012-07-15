import logging
from logging import Formatter


def logger(level='info', name='default'):
    LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    loglevel = LEVELS.get(level, logging.NOTSET)

    # Set up log format
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    format = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(format)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    logger.addHandler(ch)

    return logger
