class ApiError(BaseException):
    """Not raised explicitly, only used for grouping errors"""


class InvalidKeyError(ApiError):
    """
    Raised if the supplied API key is reported as invalid.

    Note that this may currently also be caused by server-side caching issues
    and the key may be regarded as valid on a later retry.
    """


class MissingGameAccessError(ApiError):
    """
    Raised if the account of this API key is reported as not having game access.

    This *may* indicate a temporary or permanent account suspension.
    """
