import types
import warnings
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Any, TypeGuard, TypeVar, cast

from pydantic import ValidationError, WrapValidator

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from gw2.api._base import EndpointModel, _Base
    from gw2.models import Unknown

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


def validate_enum(v: Any, handler: Callable[[Any], str]) -> "str | Unknown":
    """
    Validate (Literal) enum value,
    wrap in gw2.models.Unknown and issue warning if invalid
    """

    try:
        return handler(v)
    except ValidationError as e:
        from gw2.models import Unknown

        warnings.warn(f"failed to validate {v}: {e}", RuntimeWarning, stacklevel=2)
        return Unknown(v)


EnumValidator = WrapValidator(validate_enum)
