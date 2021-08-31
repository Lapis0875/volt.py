from logging import CRITICAL, FATAL, ERROR, WARN, WARNING, INFO, DEBUG, NOTSET
import logging
from sys import stdout

from .dtutil import kstnow


__all__ = (
    'CRITICAL',
    'FATAL',
    'ERROR',
    'WARN',
    'WARNING',
    'INFO',
    'DEBUG',
    'NOTSET',
    'get_stream_logger'
)


def get_stream_logger(name: str, stream_level: int = logging.INFO, file_level: int = logging.DEBUG) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(stream_level)

    fmt = logging.Formatter(
        style='{',
        fmt='[{asctime}] [{levelname}] {name}: {message}'
    )

    stream_handler = logging.StreamHandler(stdout)
    stream_handler.setLevel(stream_level)
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(f'logs/{kstnow().isoformat(timespec="seconds").replace(":", "-")}.txt', mode='wt', encoding='utf-8')
    logger.setLevel(file_level)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
