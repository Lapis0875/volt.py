import asyncio
import typing
from enum import Enum, auto

from .types.type_hint import JSON, CoroutineFunction


EVENT_PARAM_BUILDER = typing.Callable[[typing.Any], typing.Tuple]   # Real value : Callable[[gateway.GatewayResponse], Tuple]

class GatewayEvents(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    MESSAGE_CREATE = auto()
    MESSAGE_UPDATE = auto()
    MESSAGE_DELETE = auto()

    def register_handler(self, handler: EVENT_PARAM_BUILDER):
        if not asyncio.iscoroutinefunction(handler):
            raise TypeError(f'GatewayEvents handler must be a coroutine function, not {type(handler)}')
        setattr(self, '__handler__', handler)

    @property
    def handler(self) -> typing.Optional[EVENT_PARAM_BUILDER]:
        return getattr(self, '__handler__', None)

    @classmethod
    def event_names(cls) -> typing.Iterable[str]:
        return cls.__members__.keys()


class EventManager:
    def __init__(self, gateway):
        self.gateway = gateway
        self.listeners = {event: [] for event in GatewayEvents.event_names()}
        self.loop = asyncio.get_running_loop()

    def listen(self, event_name: str, listener: CoroutineFunction):
        if event_name not in self.listeners:
            raise ValueError(f'Cannot register listener into invalid discord gateway event {event_name}')
        if not asyncio.iscoroutinefunction(listener):
            raise TypeError(f'Event listener must be a coroutine function, not {type(listener)}')
        self.listeners[event_name].append(listener)

    def dispatch(self, resp):
        event_name, event_data = self.process_events(resp)
        listeners = self.listeners.get(event_name)
        if listeners:
            # Call listeners with proper params
            self.loop.create_task(asyncio.gather(*map(
                lambda l: l(event_data),
                listeners
            )))

    @staticmethod
    def process_events(resp) -> typing.Tuple[str, typing.Any]:
        return resp.t, None


