import logging


def make_logger(name: str, level: int):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
