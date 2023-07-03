from typing import Callable
from functools import wraps
from .logger import logging


def my_logger(msg: str = ""):
    if not msg:
        msg = f"Pending func"

    def constructor(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logging.debug(msg)
            result = await func(*args, **kwargs)
            return result

        return wrapper

    return constructor
