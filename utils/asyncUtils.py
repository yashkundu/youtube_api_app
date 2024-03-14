from asyncio import get_running_loop
from functools import partial
from typing import Callable


async def asyncWrapper(func: Callable, *args, **kwargs):
    """Runs the function in a separate thread using the ThreadPoolExecutor of the current event loop. This way we can execute synchronouse functions without blocking the current event loop."""
    task = get_running_loop().run_in_executor(None, partial(func, *args, **kwargs))
    res = await task
    return res