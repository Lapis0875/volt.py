import asyncio
import json
from enum import IntEnum, IntFlag, Enum
from random import random
from typing import Final, List

import aiohttp

from volt.events import EventManager
from volt.utils.log import get_logger, DEBUG
from volt.utils.loop_task import loop, LoopTask


class WSClosedError(Exception):
    """Exception indicating websocket closure."""

    def __init__(self, data: int):
        self.data = data
        super(WSClosedError, self).__init__(f'Websocket is closed with data {self.data}.')


class GatewayOpcodes(IntEnum):
    """
    discord gateway events.
    """
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE = 3
    VOICE_STATE = 4
    VOICE_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALIDATE_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
    GUILD_SYNC = 12

    def __repr__(self) -> str:
        return f'GatewayOpCodes.{self.name} ({self.value})'

    __str__ = __repr__


class GatewayEvents(Enum):
    READY = 'ready'


class GatewayResponse:
    __slots__ = ('op', 'data', 's', 't')

    def __init__(self, data: str):
        json_data = json.loads(data)
        self.op: GatewayOpcodes = GatewayOpcodes(json_data['op'])
        self.data = json_data.get('d')
        self.s = json_data.get('s')
        self.t = json_data.get('t')

    def __str__(self) -> str:
        return f'GatewayResponse(op={self.op.name})'

    def __getitem__(self, item):
        return self.__getattribute__(item) or None


class GatewayIntents(IntFlag):
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_BANS = 1 << 2
    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14

    @classmethod
    def all(cls) -> 'GatewayIntents':
        return GatewayIntents(sum(cls.__members__.values()))


class GatewayBot:
    def __init__(self, token: str, version: int = 9, intents: GatewayIntents = GatewayIntents.all()):
        self.logger = get_logger('volt.gateway', stream=True, stream_level=DEBUG)
        self.loop = asyncio.get_event_loop()
        self.gateway_version: Final[int] = version
        self.intents = intents
        self.__session = None
        self.__token: Final[str] = token
        self.__hearbeat_interval: int = 0
        self.__closed: bool = False
        self.__ws: aiohttp.ClientWebSocketResponse = None
        self.__last_seq = None
        self._ping = None
        self.heartbeat_sender = None
        self.event_manager = EventManager(gateway=self)

    async def connect(self):
        self.logger.debug('')
        self.__session = aiohttp.ClientSession()
        self.__ws = await self.__session.ws_connect(
            f'wss://gateway.discord.gg/?v={self.gateway_version}&encoding=json'
        )

    async def disconnect(self):
        if self.heartbeat_sender:
            self.heartbeat_sender.cancel()
        if self.__ws:
            await self.__ws.close()
        if self.__session:
            await self.__session.close()
        # Should we close event loop?

    async def identify(self):
        self.logger.debug('Send `Identify`.')
        from platform import system
        await self.__ws.send_json({
            'op': GatewayOpcodes.IDENTIFY.value,
            'd': {
                'token': self.__token,
                'intents': self.intents.value,
                'properties': {
                    '$os': system(),
                    '$browser': 'volt.py',
                    '$device': 'volt.py'
                }
            }
        })

    async def run(self):
        await self.connect()
        while not self.__closed:
            resp = await self.receive()
            self.logger.debug(f'Gateway Response : op = {resp.op}, d = {resp.data}')
            if resp.op is GatewayOpcodes.HELLO:
                # Login please!
                await self.login(resp)
            elif resp.op is GatewayOpcodes.DISPATCH:
                # Dispatch events into internal event listeners.
                self.event_manager.dispatch(resp)
            elif resp.op is GatewayOpcodes.HEARTBEAT_ACK:
                # Gateway acknowledged heartbeat.
                # TODO : Calculate ws ping.
                self._ping = None
        await self.disconnect()

    async def login(self, resp: GatewayResponse):
        # First Heartbeat
        self.__hearbeat_interval = resp.data['heartbeat_interval']
        self.__last_seq = resp.s

        @loop(seconds=self.__hearbeat_interval / 1000)
        async def heartbeat_sender(self: 'GatewayBot'):
            self.logger.debug('Sending heartbeat!')
            await self.__ws.send_json({
                'op': GatewayOpcodes.HEARTBEAT.value,
                'd': self.__last_seq or None
            })

        self.heartbeat_sender = heartbeat_sender
        self.heartbeat_sender.args = (self,)    # inject self.
        heartbeat_sender.start()

        @heartbeat_sender.before_invoke
        async def before_heartbeat_sender(self: 'GatewayBot'):
            await asyncio.sleep(self.__hearbeat_interval * random() / 1000)
            await heartbeat_sender()    # Client must send first heartbeat in heartbeat_interval * random.random() milliseconds.

        # Identify
        await self.identify()

    async def receive(self) -> GatewayResponse:
        resp = await self.__ws.receive()
        self.logger.debug(f'Raw gateway response = type = {resp.type}, data = {resp.data}')
        if resp.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSED):
            await self.disconnect()
            raise WSClosedError(resp.data or None)
        resp_obj = GatewayResponse(resp.data)
        return resp_obj

    async def close(self):
        # Stop sending heartbeats and wait to gracefully close.
        self.__closed = True
