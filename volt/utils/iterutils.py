from typing import Generator, TypeVar, Iterator, Sized, Tuple
from copy import deepcopy

T = TypeVar('T')


__all__ = (
    'SizedIter',
    'ilen',
    'chunk'
)


class SizedIter(Iterator, Sized):
    def __iter__(self) -> Iterator:
        pass

    def __next__(self):
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


def chunk(iterable: SizedIter[T], size: int) -> Generator[SizedIter[T], Tuple[int, int, SizedIter[T]], None]:
    """
    Chunk iterator of given sequence based on size parameter.
    :param iterable: Iterable object to chunk.
    :param size: Size to chunk.
    """
    for chunk_index, i in enumerate(range(0, len(iterable), size)):
        chunked = iterable[i:i + size]
        yield chunk_index, len(chunked), chunked
