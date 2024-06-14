import asyncio
from typing import Callable


async def handle_task_result(
    result_queue: asyncio.Queue, callback: Callable[[dict], None]
):
    """Result item handler
    This function (coroutine) will handle any results sitting in the result queue by
    issuing the callback.

    :param result_queue: the result queue this task consumes (pulls from)
    :param callback: the callback function to call with the results pulled from the queue
    :return:
    """
    while True:
        result = await result_queue.get()
        callback(result)
        result_queue.task_done()  # tell the queue we are done with the item
