from typing import Optional, Callable
from models import Job

Scheduler = Callable[[list[Job]], Optional[Job]]

def deadline_monotonic(jobs: list[Job]) -> Optional[Job]:
    
    shortest_deadline = None
    highest_priority_job = None
    for job in jobs:
        if (not shortest_deadline) or job.task.deadline < shortest_deadline:
            highest_priority_job = job
            shortest_deadline = job.task.deadline
            
    return highest_priority_job
   
 
def edf_scheduling(jobs: list[Job]) -> Optional[Job]:
    
    earliest_deadline = None
    highest_priority_job = None
    for job in jobs:
        if (not earliest_deadline) or job.deadline < earliest_deadline:
            highest_priority_job = job
            earliest_deadline = job.deadline
            
    return highest_priority_job 
    
    
    
rrCounter = 0
def round_robin(jobs: list[Job]) -> Optional[Job]:
    global rrCounter
    lower_task_id = rrCounter
    lower_job = None
    
    next_job_task_id = -1
    next_job = None
        
    for job in jobs:
        currTaskId = job.task.task_id 
        if(currTaskId == rrCounter):
            rrCounter = rrCounter + 1
            return job
        elif(lower_task_id > currTaskId):
            lower_job = job
            lower_task_id = job.task.task_id
        elif(currTaskId > rrCounter and (next_job == None or next_job_task_id > currTaskId)):
            next_job = job
            next_job_task_id = currTaskId
    
    
    if(next_job):
        rrCounter = next_job_task_id + 1
        return next_job
        
    if(lower_job):
        rrCounter = lower_task_id + 1
        return lower_job
        
    return None
            
