from typing import Generator, TypeVar, Iterator, Protocol
from copy import deepcopy

T = TypeVar('T')


__all__ = (
    'SizedIter',
    'ilen',
    'chunk'
)


class SizedIter(Protocol):
    def __iter__(self) -> Iterator:
        pass

    def __len__(self) -> int:
        pass


def ilen(iterable: SizedIter[T]) -> int:
    """
    Get the length of given iterable. It does not exhaust original iterable(generators)
    :param iterable: iterable to get length.
    :return: length of the iterable.
    """
    return len(deepcopy(iterable))


def chunk(iterable: SizedIter[T], size: int) -> Generator[tuple[int, int, SizedIter[T]]]:
    """
    주어진 sequence 객체를 주어진 크기로 쪼개 반환합니다.
    :param iterable: 쪼갤 반복자(Iterable) 입니다.
    :param size: 짜를 크기입니다.
    """
    for chunk_index, i in enumerate(range(0, len(iterable), size)):
        chunked = iterable[i:i + size]
        yield chunk_index, len(chunked), chunked
