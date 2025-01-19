def edf_k(tasks, num_cores, k):
    tasks.sort(key=lambda x: x['D'])
    scheduled_tasks = []
    for i, task in enumerate(tasks[:k]):
        if i < num_cores:
            scheduled_tasks.append(task)
    return scheduled_tasks
