def partitioned_edf(tasks, num_cores, heuristic, order):
    if order == "du":
        tasks.sort(key=lambda x: x['C'] / x['T'], reverse=True)
    else:
        tasks.sort(key=lambda x: x['C'] / x['T'])

    partitions = [[] for _ in range(num_cores)]
    for task in tasks:
        for partition in partitions:
            if sum(t['C'] / t['T'] for t in partition) + task['C'] / task['T'] <= 1:
                partition.append(task)
                break
    return partitions
