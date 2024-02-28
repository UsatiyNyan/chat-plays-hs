import logging


def make_logger(name: str, level: int):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger
