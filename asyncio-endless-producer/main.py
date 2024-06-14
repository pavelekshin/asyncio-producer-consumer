import asyncio
from time import perf_counter

import consumer
import producer
import resulthandler

from settings import settings


async def run() -> None:
    work_queue = asyncio.Queue(maxsize=settings.WORK_QUEUE_MAX_SIZE)
    result_queue = asyncio.Queue(maxsize=settings.RESULT_QUEUE_MAX_SIZE)

    tasks = []

    start = perf_counter()

    tasks.append(asyncio.create_task(producer.producer(work_queue), name="Producer"))

    # Create the worker (consumer) tasks
    for _ in range(settings.NUM_WORKERS):
        tasks.append(
            asyncio.create_task(
                consumer.worker(work_queue, result_queue), name=f"Worker-{_}"
            )
        )

    # Create the result handler tasks
    for _ in range(settings.NUM_RESULT_HANDLERS):
        tasks.append(
            asyncio.create_task(
                resulthandler.handle_task_result(
                    result_queue, task_completed_callback_handler
                ),
                name=f"Result handler-{_}",
            )
        )

    try:
        await asyncio.wait(tasks, timeout=10)
    finally:
        for task in tasks:
            print(f"Cancel task={task.get_name()}")
            task.cancel()

    end = perf_counter()

    # all done, callback using the provided callback function
    job_completed_callback_handler({"elapsed_secs": end - start})


def task_completed_callback_handler(callback_message: dict) -> None:
    job_id = callback_message.get("job_id")
    print(f"Task completed in {job_id=}: {callback_message=}")


def job_completed_callback_handler(callback_message: dict) -> None:
    print(f"Jobs completed: {callback_message=}")


if __name__ == "__main__":
    asyncio.run(run())
