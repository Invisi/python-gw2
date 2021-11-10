class InvalidKeyError(BaseException):
    """
    Raised if the supplied API key is reported as invalid.

    Note that this may currently also be caused by server-side caching issues
    and the key may be regarded as valid on a later retry.
    """
