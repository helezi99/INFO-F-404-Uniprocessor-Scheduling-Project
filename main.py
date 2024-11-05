# main.py
from argparse import ArgumentParser
from src.task import Task, TaskSet
from src.algorithms import EDF, DM, RoundRobin
from src.scheduler import Scheduler

def parse_arguments():
    parser = ArgumentParser(description='Real-Time Task Scheduler')
    parser.add_argument('algorithm', choices=['dm', 'edf', 'rr'], 
                       help='Scheduling algorithm to use')
    parser.add_argument('taskset_file', help='Path to task set file')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Enable verbose output')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Read task set
    taskset = TaskSet.from_file(args.taskset_file)
    
    # Select scheduling algorithm
    algorithm_map = {
        'dm': DM(),
        'edf': EDF(),
        'rr': RoundRobin()
    }
    algorithm = algorithm_map[args.algorithm]
    
    # Create scheduler
    scheduler = Scheduler(taskset, algorithm)
    
    # Check schedulability
    is_schedulable, used_simulation = scheduler.check_schedulability()
    
    if args.verbose:
        print(f"Task set is {'schedulable' if is_schedulable else 'not schedulable'}")
        print(f"{'Simulation' if used_simulation else 'Quick test'} was used")
    
    # Set appropriate exit code
    if is_schedulable:
        exit(0 if used_simulation else 1)
    else:
        exit(2 if used_simulation else 3)

if __name__ == "__main__":
    main()