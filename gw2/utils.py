import types
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, TypeGuard, TypeVar, cast

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from gw2.api._base import EndpointModel, _Base

ChunkVar = TypeVar("ChunkVar")


def chunks(lst: list[ChunkVar], n: int) -> Iterator[list[ChunkVar]]:
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


def get_generic_alias(klass: "_Base[EndpointModel]") -> types.GenericAlias:
    def type_guard(x: Any) -> TypeGuard[types.GenericAlias]:
        return hasattr(x, "__args__")

    # todo: retire and replace with types.get_original_bases on py3.12
    orig_bases = klass.__orig_bases__  # type: ignore[attr-defined]

    return cast(types.GenericAlias, next(filter(type_guard, orig_bases)))
