import math
import random
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
from fractions import Fraction
from models import TaskSet, Task, Job
from schedulers import Scheduler, deadline_monotonic, edf_scheduling, round_robin


  
def schedule(task_set: TaskSet, scheduling_function: Scheduler, t_max: int, stop_if_miss = False, ignore_history = False) -> list:  

        if scheduling_function == round_robin:
            task_set.step = 1
            
        maxOffset = 0
        for task in task_set.tasks:
            if task.offset > maxOffset:
                maxOffset = task.offset

        #to produce graph at the end
        history = []
        deadline_misses = []
        jobs = []
        for t in range(0, t_max, task_set.step):
            #check for new job releases
            for task in task_set.tasks:
                job = task.release_job(t)
                if job:
                    jobs.append(job)
                 
                 
            job_to_remove = []   
            #check for deadline misses
            for job in jobs:
                if job.deadline_missed(t):
                    #print(f"Deadline missed for job:{job} at time: {t}")
                    deadline_misses.append((t, job.task.task_id))
                    if(stop_if_miss):
                        return [history, deadline_misses]
                    job_to_remove.append(job)
                    
                    
            #remove jobs when deadline is over
            for job in job_to_remove:
                jobs.remove(job)
                    
            #schedule job with highest priority
            highest_priority_job = scheduling_function(jobs)
            if highest_priority_job:
                highest_priority_job.schedule(task_set.step)
                if not ignore_history:
                    history.append(highest_priority_job.task.task_id)
            elif not ignore_history:
                history.append(None)
                
            for job in jobs:
                if job.completed():
                    jobs.remove(job)
                    
            if scheduling_function == edf_scheduling:
                if  not jobs and maxOffset < t:
                    break;#it is an idle point, so we can stop here
                     
        return [history, deadline_misses]
    
#function used to give more weight to low numbers to avoid disproportionate values (or high number for deadlines)
def weighted_random(start: int, end: int, inv: int) -> int:
    numbers = [i for i in range(start, end +1)]
    rand = random.choices(numbers, weights=numbers[::inv],k=1)[0]
    return rand

max_adequate_computational_time = 200
max_adequate_period = 2000
def generate_task_set(task_number: int, target_utilisation: float) -> TaskSet:
  
    gen_tasks = []
    task_id = 1
    # generate tasks one by one (and leave utilisation for next task
    available_utilisation = target_utilisation / task_number
    for i in range(task_number - 1):
        
        min_ti = int(1/available_utilisation) + 1
        ti = weighted_random(min_ti, max(min_ti +20, max_adequate_period), -1)
        ci = weighted_random(1, min(max_adequate_computational_time,int(available_utilisation*ti)), -1)
        di = weighted_random(ci, ti, 1)
        gen_tasks.append(Task(task_id, 0, ci, di, ti))
        task_id +=1
        available_utilisation = available_utilisation - ci/ti + target_utilisation / task_number
        
    #choose best fit for the last task:
    last_frac = Fraction(available_utilisation).limit_denominator(max_adequate_period)
    cn = last_frac.numerator
    tn = last_frac.denominator
    
    # make sure that we do not exceed the target utilisation
    while(available_utilisation < cn/tn):
        if(cn>1):
            cn-=1
        else:
            tn +=1
    dn = weighted_random(cn, tn, 1)
    gen_tasks.append(Task(task_id, 0, cn, dn, tn))
    
    return TaskSet(gen_tasks)
    
    
def read_task_set_file(filename: str) -> TaskSet:
    ts_file = open(filename, "r")
    tasks = []
    
    task_id_ctr = 0
    for line in ts_file.readlines():
        values = [int(num) for num in line.split(" ")]
        task = Task(task_id_ctr, *values)    
        tasks.append(task)    
        task_id_ctr +=1
    
    return TaskSet(tasks)
    
def write_task_set_file(filename: str, task_set: TaskSet):
    with open(filename, "w") as ts_file:   
        for task in task_set.tasks:
            line = f"{task.offset} {task.compute_time} {task.deadline} {task.period}\n"
            ts_file.write(line)

  
def get_feasibility_interval(scheduler, taskset):
    periods = [task.period  for task in taskset.tasks]
    hyperPeriod = math.lcm(*periods)
    #get Omax
    maxOffset = 0
    for task in taskset.tasks:
        if task.offset > maxOffset:
            maxOffset = task.offset
            
    if scheduler == round_robin:
        return hyperPeriod
        
    elif maxOffset == 0:#synchronous: use max deadline
        deadlines = [task.deadline for task in taskset.tasks]
        if(len(deadlines) == 1):
            maxDeadline = deadlines[0]
        else:
            maxDeadline = max(*deadlines)
        return maxDeadline
    elif scheduler == edf_scheduling:# asynchronous but we assume constrained deadlines
         # [0, Omax + 2P) is a feasibility interval for edf if U(T)<1 
         return 2*hyperPeriod + maxOffset
    elif scheduler == deadline_monotonic:
        s_i = taskset.tasks[0].offset
        for i, task in enumerate(taskset.tasks[1:]):
            duration = math.max(s_i - task.offset, 0)
            s_i = task.offset + math.ceil(duration/task.period) * task.period
        return s_i + hyperPeriod
    assert False
      
  
    
def plot_scheduling(history: list, task_set: TaskSet, save_file=None):

    deadline_misses = history[1]
    history = history[0]
    #plt.arrow(x,y,dx,dy)
    n = len(task_set.tasks)  
    
    t_max = len(history*task_set.step)  
    
    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=n-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    
    
    # Horizontal bar plot with gaps
    fig, ax = plt.subplots()
    num = 0
    for task in task_set.tasks:
        tID = task.task_id
        intervals = []
        intervalBeginning = -1
        
        for i in range(len(history)):
            if history[i] == tID:
                if intervalBeginning == -1:
                    intervalBeginning = i*task_set.step
            elif intervalBeginning != -1:
                intervals.append((intervalBeginning, i*task_set.step- intervalBeginning))
                intervalBeginning = -1
                
        if(intervalBeginning != -1):
            intervals.append((intervalBeginning, (i+1)*task_set.step- intervalBeginning))
        
        ax.broken_barh(intervals, ((num+1)*10 - 4, 8), facecolors=scalarMap.to_rgba(num))
        
        release_time = task.offset
        #print release and deadlines
        while release_time <= t_max:
            ax.arrow(release_time, (num+1)*10+5,0,-3, width=0.2, facecolor='black')
            ax.add_patch(plt.Circle((release_time + task.deadline, (num+1)*10), radius=0.5, facecolor='none', edgecolor='black'))
            release_time += task.period
        
        num+=1
    for miss in deadline_misses:
        time = miss[0]
        task_id = miss[1]
        ax.plot(time, (task_id+1)*10, "X", color='red')
    #ax.set_ylim(5, 35)
    ax.set_xlim(0, t_max)
    ax.set_xlabel('time steps')
    ax.set_yticks([(num+1)*10 for num in range(n)], labels=[f"Task{task.task_id}" for task in task_set.tasks])     # Modify y-axis tick labels
    ax.grid(True)                                       # Make grid lines visible
    #ax.annotate('race interrupted', (61, 25), xytext=(0.8, 0.9), textcoords='axes fraction', arrowprops=dict(facecolor='black', shrink=0.05), fontsize=16, horizontalalignment='right', verticalalignment='top')
    if(not save_file):
        plt.show()
    else:
        plt.savefig(save_file)

                    
          
