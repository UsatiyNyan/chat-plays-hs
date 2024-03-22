import logging


def make_logger(name: str, level: int):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(logging.FileHandler(f'{name}.log'))
    logger.addHandler(logging.StreamHandler())
    return logger
