import asyncio
from random import randrange
from uuid import uuid4


async def data_generator(start: int, job_id: str):
    return [
        {"task_id": i, "number": i, "uuid": job_id}
        for i in range(start + randrange(10))
    ]


async def producer(work_queue: asyncio.Queue):
    """
    Puts all the requested work into the work queue.

    :param work_queue: main work queue that contains each individual task params
    :return:
    """
    start = 0
    while True:
        job_id = str(uuid4())
        print(f"New Job {job_id}")
        for data in await data_generator(start, job_id):
            await work_queue.put(data)
        await asyncio.sleep(1)
        start += randrange(10)
