from collections import Iterator
from typing import List, TypeVar

ChunkVar = TypeVar("ChunkVar")


def chunks(lst: List[ChunkVar], n: int) -> Iterator[List[ChunkVar]]:
    """
    Yield successive n-sized chunks from lst.

    Args:
        lst: List of any object
        n: The size of a chunk
    Returns:
        An iterator for lists of n-sized chunks
    """

    for i in range(0, len(lst), n):
        yield lst[i : i + n]
