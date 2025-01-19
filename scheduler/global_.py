from heapq import heappush, heappop

def global_edf(tasks, num_cores):
    ready_queue = []
    for task in tasks:
        heappush(ready_queue, (task['D'], task))

    scheduled_tasks = []
    for _ in range(num_cores):
        if ready_queue:
            _, task = heappop(ready_queue)
            scheduled_tasks.append(task)
    return scheduled_tasks