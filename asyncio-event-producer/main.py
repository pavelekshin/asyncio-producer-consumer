from functools import partial
from random import seed
from uuid import uuid4

from controller import run_job


def main(job_id: str) -> None:
    """
    Main app that kicks a "job" that consists of running multiple tasks

    :param job_id: some job identifier
    :return:
    """

    print(f"Starting Job {job_id}")

    # define callbacks, "injecting" the job_id
    task_callback = partial(task_completed_callback_handler, job_id)
    job_callback = partial(job_completed_callback_handler, job_id)

    # define the parameters for the tasks that will need to run
    task_data = [{"task_id": i, "number": i} for i in range(100)]

    # start job
    run_job(task_data, task_callback, job_callback)


def task_completed_callback_handler(job_id: str, callback_message: dict) -> None:
    print(f"Task completed in {job_id=}: {callback_message=}")


def job_completed_callback_handler(job_id: str, callback_message: dict) -> None:
    print(f"Job {job_id} completed: {callback_message=}")


if __name__ == "__main__":
    seed(0)
    main(str(uuid4()))
