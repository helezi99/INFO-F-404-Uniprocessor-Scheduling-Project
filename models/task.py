from dataclasses import dataclass


@dataclass
class Task:
    task_id: int
    offset: int
    compute_time: int
    deadline: int
    period: int
    jobs_released: int

    def __init__(self, task_id: int, offset: int, compute_time: int, deadline: int, period: int):
        self.task_id = task_id
        self.offset = offset
        self.compute_time = compute_time
        self.deadline = deadline
        self.period = period
        self.jobs_released = 0

    def release_job(self, time: int):
        # Avoid circular imports
        from .job import Job

        # Release a job is the time is a multiple of the period
        if (time - self.offset) % self.period == 0:
            self.jobs_released += 1
            return Job(self, time + self.deadline, self.compute_time, self.jobs_released)
            
    def __str__(self):
        return f"[Task{self.task_id} O:{self.offset} C:{self.compute_time} D:{self.deadline} T:{self.period}]"
