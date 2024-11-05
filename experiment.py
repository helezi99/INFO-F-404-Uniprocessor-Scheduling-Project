from core import generate_task_set, write_task_set_file, get_feasibility_interval, schedule
from schedulers import Scheduler, deadline_monotonic, edf_scheduling, round_robin
import random

random.seed(42)
directory = "./dataset"

schedulers = [deadline_monotonic, edf_scheduling, round_robin]
results_task = [[0]*30 for i in range(len(schedulers))]
results_utilisation = [[0]*20 for i in range(len(schedulers))]

for task_num in range(1, 31):
    for utilisation_step in range(1, 20):
        target_utilisation = utilisation_step * 0.05
        print(f"Schedule for {task_num} tasks and target utilisation of {target_utilisation:.2f}") 
        task_set = generate_task_set(task_num, target_utilisation)
        print(task_set)
        
        total_utilisation = 0
        for task in task_set.tasks:
            total_utilisation += task.compute_time / task.period
        print("Utilisation:", total_utilisation)
        
        #save dataset in files
        #write_task_set_file(f"{directory}/taskset{task_num}_{target_utilisation:.2f}", task_set)
        idx_scheduler = 0
        for scheduler in schedulers:
            t_max = get_feasibility_interval(scheduler, task_set)
            print("Feasibily interval: [0,",t_max, "]")
            history = schedule(task_set, scheduler, min(t_max, 100000), True, True)
            
            if not history[1]:#no deadline misses
                results_task[idx_scheduler][task_num -1] += 1
                results_utilisation[idx_scheduler][utilisation_step -1] += 1
            idx_scheduler+=1
                
        
for i in range(len(schedulers)):
    results_task[i] = [num / 20 for num in results_task[i]]
    results_utilisation[i] = [num / 30 for num in results_utilisation[i]]


print(results_task)
print(results_utilisation)

