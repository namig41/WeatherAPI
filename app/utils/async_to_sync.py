import asyncio
from functools import wraps


def async_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(func(*args, **kwargs), loop)
            return future.result()
        else:
            return asyncio.run(func(*args, **kwargs))

    return wrapper
