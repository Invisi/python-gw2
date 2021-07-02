import httpx


class InvalidKeyError(httpx.HTTPStatusError):
    pass
