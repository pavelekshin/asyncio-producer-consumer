import asyncio
from time import perf_counter
from typing import Callable, List

import consumer
import producer
import resulthandler

from settings import settings


async def controller(
    batch: List[dict],
    task_completed_callback: Callable,
    job_completed_callback: Callable,
) -> None:
    """
    This is the async controller.

    :param batch: a list of dictionaries received that defines the parameters for each task that has to run
    :param task_completed_callback: the callback to use when each task result becomes available
    :param job_completed_callback: the callback to use when the overall job is completed
    :return:
    """
    start = perf_counter()

    # create the work and result queues
    work_queue = asyncio.Queue(maxsize=settings.WORK_QUEUE_MAX_SIZE)
    result_queue = asyncio.Queue(maxsize=settings.RESULT_QUEUE_MAX_SIZE)

    # create a list of all the tasks that will need to run async
    tasks = []

    # Define the producer task, defining the event we'll look for when the producer is done
    producer_completed = asyncio.Event()

    tasks.append(
        asyncio.create_task(producer.producer(batch, work_queue, producer_completed))
    )

    # Create the worker (consumer) tasks
    for _ in range(settings.NUM_WORKERS):
        tasks.append(asyncio.create_task(consumer.worker(work_queue, result_queue)))

    # Create the result handler tasks
    for _ in range(settings.NUM_RESULT_HANDLERS):
        tasks.append(
            asyncio.create_task(
                resulthandler.handle_task_result(result_queue, task_completed_callback)
            )
        )

    # Now wait completion of producer, and kick off the consumers and result handlers
    await producer_completed.wait()
    await work_queue.join()
    await result_queue.join()

    # once we reach here, we're all done, so cancel all tasks
    for task in tasks:
        task.cancel()

    end = perf_counter()

    # all done, callback using the provided callback function
    job_completed_callback({"elapsed_secs": end - start})
