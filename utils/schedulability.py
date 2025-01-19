def calculate_utilization(tasks):
    """
    Calculate total utilization of a taskset.
    U = sum(Ci / Ti) for all tasks i.
    """
    return sum(task['C'] / task['T'] for task in tasks)

def check_necessary_condition(tasks):
    """
    Check the necessary condition for schedulability: U <= 1.
    """
    utilization = calculate_utilization(tasks)
    return utilization <= 1

def check_sufficient_condition(tasks, m):
    """
    Check a sufficient condition for schedulability on m cores.
    """
    # Example sufficient condition for partitioned EDF
    # If U <= m * (2^(1/m) - 1), then schedulable
    from math import pow
    utilization = calculate_utilization(tasks)
    bound = m * (pow(2, 1 / m) - 1)
    return utilization <= bound

def simulate_taskset(tasks, interval):
    """
    Simulate the taskset over a given time interval.
    Return True if no deadlines are missed, otherwise False.
    """
    # Example: Dummy simulation logic
    # Iterate over the interval and check for deadline misses
    for time in range(interval[0], interval[1] + 1):
        for task in tasks:
            if time % task['T'] == task['D'] and time < task['O'] + task['C']:
                return False  # Deadline missed
    return True

def determine_schedulability(tasks, m, interval=None):
    """
    Determine schedulability of a taskset:
    - Check necessary condition.
    - Check sufficient condition.
    - Simulate if necessary.
    """
    if not check_necessary_condition(tasks):
        return 3  # Necessary condition not met

    if check_sufficient_condition(tasks, m):
        return 1  # Sufficient condition met

    if interval:
        if simulate_taskset(tasks, interval):
            return 0  # Schedulable with simulation
        else:
            return 2  # Not schedulable, simulation required

    return 4  # Unable to determine
