from dataclasses import dataclass
import math
from .task import Task
from .job import Job


@dataclass
class TaskSet:
    tasks: list[Task]
    step: int
    
    def __init__(self, tasks):
        self.tasks = tasks
        
        # compute best step with gcd (careful of the offset)
        step = None
        for task in tasks:
            if not step:
                step = task.offset
                
            step = math.gcd(step, task.offset, task.compute_time, task.deadline, task.period)
        
        if not step:# no tasks
            step = 1
        
        self.step = step

        
    def __str__(self):
        res = "Taskset:\n"
        for task in self.tasks:
            res+=str(task) + "\n"
        return res
