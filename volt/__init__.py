"""
volt
~~~~~~~~~~~~~~~~~~~

A basic wrapper for the Discord API.
:copyright: (c) 2015-present Lapis0875
:license: MIT, see LICENSE for more details.
"""

__title__ = 'volt'
__author__ = 'Lapis0875'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-present Lapis0875'
__version__ = '0.1.0'

import os

from .abc import Snowflake, Subscribable
from .embed import *
from . import utils, ext


logger = utils.get_logger('volt', stream_level=utils.INFO)

# Speedups
if os.name != 'nt':
    # Since uvloop is not supported on windows platform, I need to check
    try:
        import uvloop
        logger.debug('Found module `uvloop`. Set asyncio`s event loop policy to uvloop.EventLoopPolicy.')
        uvloop.install()
        logger.debug('Installed and applied uvloop.')
    except ModuleNotFoundError:
        logger.debug('`uvloop` module not found. Skip event loop speedups.')

