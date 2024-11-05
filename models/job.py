from dataclasses import dataclass
from .task import Task


@dataclass
class Job:
    task: Task
    deadline: int
    remaining_time: int
    job_id: int

    def deadline_missed(self, time: int) -> bool:
        return time >= self.deadline and self.remaining_time > 0

    def schedule(self, num_steps: int):
        self.remaining_time -= num_steps

    def completed(self) -> bool:
        return self.remaining_time <= 0
    
    def __str__(self):
        return f"[Job{self.job_id} task:{self.task.task_id}, remaining time:{self.remaining_time}, deadline:{self.deadline}]" 
