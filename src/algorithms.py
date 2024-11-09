# src/algorithms.py
from abc import ABC, abstractmethod

class SchedulingAlgorithm(ABC):
    @abstractmethod
    def get_priority(self, task, current_time):
        """Returns the priority of the task"""
        pass
        
    @abstractmethod
    def schedule_next_job(self, task, current_time):
        """Schedules the next job for the task"""
        pass
        
    @abstractmethod
    def quick_test(self, taskset):
        """Checks if schedulability can be determined through quick test"""
        pass


class EDF(SchedulingAlgorithm):
    def get_priority(self, task, current_time):
        return -task.get_absolute_deadline(current_time)

    def schedule_next_job(self, task, current_time):
        if current_time <= task.offset:
            task.next_release = task.offset
            task.next_deadline = task.offset + task.deadline
        else:
            current_period = ((current_time - task.offset) // task.period) + 1
            task.next_release = task.offset + current_period * task.period
            task.next_deadline = task.next_release + task.deadline
        task.remaining_time = task.computation_time

    def get_time_to_next_event(self, current_task, current_time, next_releases):
        """EDF is preemptive, need to consider new task release"""
        if not next_releases:
            return current_task.remaining_time
        return min(
            current_task.remaining_time,
            min(r - current_time for r in next_releases)
        )
        
    def utilization_lt_1(self, taskset):
        """EDF: For implicit deadline taskset, utilization <= 1 is sufficient"""
        utilization = sum(task.computation_time / task.period for task in taskset)
        return utilization >= 1
    
    def is_implicit(self, taskset):
        is_implicit = all(task.deadline == task.period for task in taskset)
        return is_implicit 
        
    def quick_test(self, taskset):
        """EDF: Non-implicit deadline taskset needs simulation"""
        if self.utilization_lt_1(taskset):
            return False, False
        elif self.is_implicit(taskset):
            return True, False
        else:
            return None, True

class DM(SchedulingAlgorithm):
    def get_priority(self, task, current_time):
        """Returns the priority of the task"""
        pass
        
    def schedule_next_job(self, task, current_time):
        """Schedules the next job for the task"""
        pass
        
    def quick_test(self, taskset):
        """Performs exact response time analysis for DM schedulability test
        Returns: (schedulable, needs_simulation)
        """
        # First sort tasks by deadline (DM priority assignment)
        sorted_tasks = sorted(taskset, key=lambda t: t.deadline)
        
        # Calculate worst-case response time for each task
        for i, task_i in enumerate(sorted_tasks):
            # Initialize w0 = Ci
            w_k = task_i.computation_time
            
            while True:
                # Calculate w_(k+1)
                w_k1 = task_i.computation_time
                # Consider interference from all higher priority tasks
                for j in range(i):
                    task_j = sorted_tasks[j]
                    # Calculate interference term: ceil(w_k/Tj) * Cj
                    interference = ((w_k + task_j.period - 1) // task_j.period) * task_j.computation_time
                    w_k1 += interference
                
                # Check termination conditions
                if w_k1 > task_i.deadline:
                    # Response time exceeds deadline, not schedulable
                    return False, False
                if w_k1 == w_k:
                    # Found exact value, check next task
                    break
                
                w_k = w_k1
                
        # All tasks' response times are within deadlines
        return True, False

class RoundRobin(SchedulingAlgorithm):
    def __init__(self):
        self.time_quantum = 1  # Set time quantum to 1
        self.last_execution = {}  # Record the last execution time of each task
        
    def get_priority(self, task, current_time):
        """Return priority based on last execution time, tasks executed earlier have higher priority"""
        return -(self.last_execution.get(task, -float('inf')))
        
    def schedule_next_job(self, task, current_time):
        if current_time <= task.offset:
            task.next_release = task.offset
            task.next_deadline = task.offset + task.deadline
        else:
            current_period = ((current_time - task.offset) // task.period) + 1
            task.next_release = task.offset + current_period * task.period
            task.next_deadline = task.next_release + task.deadline
        task.remaining_time = task.computation_time
        
    def get_time_to_next_event(self, current_task, current_time, next_releases):
        """Update task's last execution time after its time quantum"""
        time_to_next = min(
            self.time_quantum,
            current_task.remaining_time
        )
        self.last_execution[current_task] = current_time + time_to_next
        return time_to_next

    def quick_test(self, taskset):
        """Only perform utilization test, feasibility interval is P"""
        utilization = sum(task.computation_time / task.period for task in taskset)
        if utilization > 1:
            return False, False
        else:
            return None, True  # Simulation needed to determine schedulability