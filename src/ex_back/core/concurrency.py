import uuid
from concurrent.futures import ProcessPoolExecutor
from enum import Enum


class JobStatus(Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class JobRunner:
    def __init__(self, max_workers=None):
        self.executor = ProcessPoolExecutor(max_workers=max_workers)
        self.jobs = {}  # to store Future objects

    def run(self, fn, *args, **kwargs):
        job_id = str(uuid.uuid4())
        future = self.executor.submit(fn, *args, **kwargs)
        self.jobs[job_id] = future
        return job_id

    def check_status(self, job_id):
        if job_id not in self.jobs:
            raise ValueError(f"No job with ID {job_id}")

        future = self.jobs[job_id]
        if future.running():
            return JobStatus.RUNNING
        elif future.done():
            if future.exception() is not None:
                return JobStatus.FAILED
            else:
                return JobStatus.COMPLETED
        else:
            return JobStatus.IDLE

    def shutdown(self):
        self.executor.shutdown(wait=True)
