from functools import wraps
from typing import Callable


def transaction(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        commit = kwargs.pop("_commit", True)
        result = await func(*args, **kwargs)

        self = args[0]

        if commit:
            await self.session.commit()
        else:
            await self.session.flush()

        return result

    return wrapper


def duplicate(detail: str = None):
    def constructor(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            return result

        return wrapper

    return constructor
