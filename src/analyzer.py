# src/analyzer.py
import os
from pathlib import Path
from typing import Dict, List, Tuple
from .task import TaskSet
from .algorithms import DM, EDF, RoundRobin
from .scheduler import Scheduler

class SchedulabilityAnalyzer:
    def __init__(self):
        self.algorithms = {
            'dm': DM(),
            'edf': EDF(),
            'rr': RoundRobin()
        }
        
    def analyze_taskset(self, taskset_path: str) -> Dict[str, bool]:
        """Analyze schedulability of a single task set"""
        taskset = TaskSet.from_file(taskset_path)
        results = {}
        
        # Test each algorithm
        for alg_name, algorithm in self.algorithms.items():
            scheduler = Scheduler(taskset, algorithm)
            is_schedulable, _ = scheduler.check_schedulability()
            results[alg_name] = is_schedulable
            
        return results

    def collect_directory_data(self, directory: str) -> Dict[str, Dict]:
        """Collect data for all task sets in the specified directory"""
        path = Path(directory)
        results = {
            'total': 0,
            'feasible': 0,
            'dm_schedulable': 0,
            'edf_schedulable': 0,
            'rr_schedulable': 0
        }
        
        # Traverse all task set files in the directory
        for taskset_file in path.glob('taskset-*'):
            results['total'] += 1
            taskset_results = self.analyze_taskset(str(taskset_file))
            
            # Count schedulable sets
            schedulable_count = sum(taskset_results.values())
            if schedulable_count > 0:
                results['feasible'] += 1
            
            # Count schedulable sets for each algorithm
            for alg_name, is_schedulable in taskset_results.items():
                if is_schedulable:
                    results[f'{alg_name}_schedulable'] += 1
                    
        return results

    def analyze_by_task_number(self, base_dir: str) -> Dict:
        """Analyze data for different task numbers in the 80-percent directory"""
        task_number_data = {
            'task_counts': [],
            'results': {}
        }
        
        # Traverse subdirectories in the 80-percent directory
        base_path = Path(base_dir)
        for subdir in base_path.glob('*-tasks'):
            task_count = int(subdir.name.split('-')[0])
            task_number_data['task_counts'].append(task_count)
            task_number_data['results'][task_count] = self.collect_directory_data(str(subdir))
            
        # Sort task count list
        task_number_data['task_counts'].sort()
        return task_number_data

    def analyze_by_utilization(self, base_dir: str) -> Dict:
        """Analyze data for different utilization rates in the 10-tasks directory"""
        utilization_data = {
            'utilizations': [],
            'results': {}
        }
        
        # Traverse subdirectories in the 10-tasks directory
        base_path = Path(base_dir)
        for subdir in base_path.glob('*-percent'):
            utilization = int(subdir.name.split('-')[0])
            utilization_data['utilizations'].append(utilization)
            utilization_data['results'][utilization] = self.collect_directory_data(str(subdir))
            
        # Sort utilization list
        utilization_data['utilizations'].sort()
        return utilization_data

    def calculate_success_rates(self, results: Dict) -> Dict[str, float]:
        """Calculate success rates"""
        if results['feasible'] == 0:
            return {
                'dm': 0.0,
                'edf': 0.0,
                'rr': 0.0
            }
            
        return {
            'dm': results['dm_schedulable'] / results['feasible'],
            'edf': results['edf_schedulable'] / results['feasible'],
            'rr': results['rr_schedulable'] / results['feasible']
        }

def main():
    analyzer = SchedulabilityAnalyzer()
    
    # Analyze data based on number of tasks
    task_number_data = analyzer.analyze_by_task_number('tasksets/80-percent')
    
    # Analyze data based on utilization rates
    utilization_data = analyzer.analyze_by_utilization('tasksets/10-tasks')
    
    # Save data (can be saved as JSON or other formats)
    import json
    with open('analysis_results.json', 'w') as f:
        json.dump({
            'task_number_data': task_number_data,
            'utilization_data': utilization_data
        }, f, indent=2)

if __name__ == '__main__':
    main()