from core import schedule, plot_scheduling, read_task_set_file, get_feasibility_interval
from schedulers import deadline_monotonic, edf_scheduling, round_robin
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("scheduler", choices=['dm','edf','rr'], help="The scheduler to use")
parser.add_argument("taskset_file", help="The file containing the task set")

args = parser.parse_args()

taskset = read_task_set_file(args.taskset_file)
shedulers = {"dm": deadline_monotonic, "edf": edf_scheduling, "rr" : round_robin}
scheduler = shedulers[args.scheduler]
t_max = get_feasibility_interval(scheduler, taskset)

history = schedule(taskset, scheduler, t_max)
plot_scheduling(history, taskset, args.taskset_file + ".png")

if scheduler == edf_scheduling:
    total_utilisation = 0
    
    for task in taskset.tasks:
        total_utilisation += task.compute_time / task.period

    if total_utilisation > 1:
        exit(1)

if not history[1]:
    exit(0)
else:
    exit(1)
