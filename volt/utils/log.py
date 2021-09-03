from logging import CRITICAL, FATAL, ERROR, WARN, WARNING, INFO, DEBUG, NOTSET
import logging
from sys import stdout
from os import path, mkdir
from .dtutil import utcnow


__all__ = (
    'CRITICAL',
    'FATAL',
    'ERROR',
    'WARN',
    'WARNING',
    'INFO',
    'DEBUG',
    'NOTSET',
    'get_logger'
)


def get_logger(name: str, stream: bool = True, stream_level: int = logging.INFO, file: bool = False, file_level: int = logging.DEBUG) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(stream_level)

    fmt = logging.Formatter(
        style='{',
        fmt='[{asctime}] [{levelname}] {name}: {message}'
    )

    if stream:
        stream_handler = logging.StreamHandler(stdout)
        stream_handler.setLevel(stream_level)
        stream_handler.setFormatter(fmt)
        logger.addHandler(stream_handler)

    if file:
        if not path.exists('./logs'):
            mkdir('./logs')
        file_handler = logging.FileHandler(f'logs/{utcnow().isoformat(timespec="seconds").replace(":", "-")}.txt', mode='wt', encoding='utf-8')
        logger.setLevel(file_level)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger
