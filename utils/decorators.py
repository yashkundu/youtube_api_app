from functools import wraps
import asyncio


def repeatEvery(seconds: float):
    """Creates a decorator which reruns the wrapped coroutines between the specified intervals indefinitely

    Args:
        seconds (float): The amount of seconds between which the coroutine should be run.
    """
    def decorator(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            async def loop():
                while True:
                    await func(*args, **kwargs)
                    await asyncio.sleep(delay=seconds)
            asyncio.ensure_future(loop())
        return wrapped
    return decorator

