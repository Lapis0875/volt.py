from typing import Dict, Union, Callable, Coroutine, Protocol, Any, Literal

__all__ = (
    'JSON',
    'Function',
    'CoroutineFunction',
    'AnyFunction',
    'JsonCompatObject'
)

JSON = Dict[str, Union[str, int, float, bool, list, dict, None]]
Function = Callable[..., Any]
CoroutineFunction = Callable[..., Coroutine]
AnyFunction = Union[Function, CoroutineFunction]

RestMethod = Literal['GET', 'POST', 'PATCH', 'DELETE']
FileMode = Literal[
    'w', 'wt', 'wb', 'w+', 'w+t', 'w+b',
    'r', 'rt', 'rb', 'r+', 'r+t', 'r+b',
    'a', 'at', 'ab', 'a+', 'a+t', 'a+b',
    'x', 'xt', 'xb', 'x+', 'x+t', 'x+b',
]


class JsonCompatObject(Protocol):
    @classmethod
    def from_json(cls, data: JSON): ...

    def to_json(self) -> JSON:  ...
