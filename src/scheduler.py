# src/scheduler.py
class SchedulerError(Exception):
    """Scheduler related exceptions"""
    pass

class Scheduler:
    def __init__(self, taskset, algorithm):
        self.taskset = taskset
        self.algorithm = algorithm
        self.current_time = 0
        
    def check_schedulability(self):
        """Check if the task set is schedulable"""
        # First check if we can determine through quick test
        schedulable, needs_simulation = self.algorithm.quick_test(self.taskset)
        if schedulable is None:
            return self._simulate(), needs_simulation
        elif schedulable:
            return True, False
        else:
            return False, False
            
        # Check if simulation is needed
        if not self.algorithm.needs_simulation(self.taskset):
            return False, False
            
        # Perform simulation
        return self._simulate(), True
    
    def _simulate(self):

        simulation_length = self._calculate_simulation_length()
        self.current_time = 0
        
        # Initialize all tasks
        for task in self.taskset:
            self.algorithm.schedule_next_job(task, self.current_time)
        
        while self.current_time < simulation_length:
            # Get currently runnable tasks
            ready_tasks = [task for task in self.taskset 
                          if task.is_ready(self.current_time) and 
                          task.remaining_time > 0]
            
            if not ready_tasks:
                # No ready tasks, advance to next release time
                next_release = min((task.next_release for task in self.taskset 
                                  if task.next_release > self.current_time),
                                 default=simulation_length)
                self.current_time = next_release
                continue
            
            # Select the highest priority task
            # Different scheduling algorithms implement different priority strategies via get_priority method
            selected_task = max(ready_tasks,
                              key=lambda t: self.algorithm.get_priority(t, self.current_time))
            
            # Calculate time to next event
            # For preemptive scheduling (like EDF, DM), consider new task release times
            # For non-preemptive scheduling (like some RR variants), might only need to consider
            # current task completion time or time slice
            time_to_next_event = self.algorithm.get_time_to_next_event(
                selected_task, 
                self.current_time,
                [t.next_release for t in self.taskset if t.next_release > self.current_time]
            )
            
            # Update time and remaining execution time
            self.current_time += time_to_next_event
            selected_task.remaining_time -= time_to_next_event
            
            # Check if deadline is missed
            if self.current_time > selected_task.next_deadline:
                return False
                
            # If task completed, schedule next job
            if selected_task.remaining_time == 0:
                 self.algorithm.schedule_next_job(selected_task, self.current_time)
        
        return True
    
    def _calculate_simulation_length(self):
        """
        Calculate the length of feasibility interval
        Returns the fixed point L such that schedulability in [0,L) determines
        schedulability of the entire task set
        
        Raises:
            SchedulerError: if iteration does not converge
        """
        # Initialize w0 = sum of computation times of all tasks
        w_k = sum(task.computation_time for task in self.taskset)
        
        # Iterate until fixed point is found
        while True:
            # Calculate w_{k+1}
            w_next = sum(
                ((w_k + task.period - 1) // task.period) * task.computation_time
                for task in self.taskset
            )
            
            # If fixed point found, this is our feasibility interval length
            if w_next == w_k:
                return w_k
                
            # If w_{k+1} > w_k, continue iteration
            if w_next > w_k:
                w_k = w_next
            else:
                # Iteration did not converge, this should not happen
                raise SchedulerError("Failed to compute feasibility interval: iteration did not converge")