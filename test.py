from schedulers import rate_monotonic, edf_scheduling, round_robin
from models import TaskSet, Task, Job
from core import schedule, print_history, plot_scheduling, generate_task_set, read_task_set_file


ts1 = read_task_set_file("task_set1")

print(ts1)

task1 = Task(0,4,2,6,6)
task2 = Task(1,0,3,8,8)
task3 = Task(2,7,2,6,25)
taskS = [task1, task2,task3]
task_set = TaskSet(taskS)

history_rm = schedule(task_set, rate_monotonic, 150)
print("Rate monotonic: ")
print(history_rm)
plot_scheduling(history_rm, task_set, 150)
assert False

history_edf = schedule(task_set, edf_scheduling, 150)
print("Earliest deadline first: ")
print_history(history_edf, task_set,150)

#same with step of 2
task3 = Task(0,8,4,12,12)
task4 = Task(1,0,6,16,16)
task5 = Task(2,14,4,12,50)
taskS = [task3,task4,task5]
task_set2 = TaskSet(taskS)

history_edf2 = schedule(task_set2, edf_scheduling, 150)
print(f"Earliest deadline first (with step {task_set2.step}): ")
print_history(history_edf2, task_set2,150)

rrCounter = 0

task_set3 = generate_task_set(10,0.8)
print(task_set3)
history_edf3 = schedule(task_set3, round_robin, 2000)
print(f"Round robin with generated task set and step {task_set3.step}: ")
print_history(history_edf3, task_set3,2000)

"""
Tests :
"""

def test_release_job():
    task1 = Task(0,5,15,25)
    task2 = Task(1,10,100,100)
    
    print(task1, task2)
    
    for i in range(200):
        newJob = task1.release_job(i)
        if not newJob:
            newJob = task2.release_job(i)
        if newJob:
            print(f"{newJob} at time: {i}")


def test_all(task_set):
    test_release_job()
    
    
#test_all(task_set)
