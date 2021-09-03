"""
Aware Datetime Utility
"""

import datetime
from typing import Union


__all__ = (
    'UTC',
    'utcnow',
    'get_discord_timestamp',
    'is_leap_year'
)

UTC = datetime.timezone.utc


def utcnow() -> datetime.datetime:
    return datetime.datetime.utcnow().replace(tzinfo=UTC)


def get_discord_timestamp(dt: datetime.datetime, style: str = None):
    """
    Convert datetime object into discord's timestamp expression.
    :param dt: datetime object to convert.
    :param style: timestamp style. default is None.
    :return: string value of timestamp expression.
    """
    if dt is None:
        return 'UNDEFINED'
    if dt.tzinfo is None:
        dt = UTC.localize(dt)
    elif dt.isoformat().split('+')[1] == '00:00':   # UTC
        dt = dt.replace(tzinfo=UTC)

    return f'(KST) <t:{int(dt.timestamp())}' + (f':{style}>' if style else '>')


def is_leap_year(year: int) -> bool:
    """
    Check if given year is leap year. (February has 29th date!)
    :param year: Year to check whether it is leap year or not.
    :return: boolean value indicating if the given year is leap year.
    """
    mod4 = year % 4 == 0
    mode100 = year % 100 == 0
    mod400 = year % 400 == 0
    if mod400:
        # Year when mod 4, mod 100, mod 400 are all 0 is a leap year.
        return True
    elif mode100 and mod4:
        # Year when mod 400 isn't 0 and mod 4, mod 100 are all 0 is not a leap year.
        return False
    elif not mode100 and mod4:
        # Year when mod 100 isn't 0 and mod 4 is 0 is a leap year.
        return True
    else:
        # Just yet another regular year!
        return False
