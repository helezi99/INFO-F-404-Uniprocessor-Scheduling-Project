# src/plotter.py
import matplotlib.pyplot as plt
import json

class Plotter:
    def __init__(self):
        # print(plt.style.available) 
        plt.style.use('bmh')  
        self.colors = {
            'dm': '#2ecc71',    
            'edf': '#3498db',  
            'rr': '#e74c3c'     
        }
        plt.rcParams.update({'font.size': 12})
        
    def plot_feasibility_by_tasks(self, data):
        """Plot relationship between number of tasks and feasibility ratio"""
        task_counts = data['task_counts']
        feasibility_ratios = []
        
        for count in task_counts:
            results = data['results'][str(count)]
            ratio = results['feasible'] / results['total']
            feasibility_ratios.append(ratio)
            
        plt.figure(figsize=(10, 6))
        plt.plot(task_counts, feasibility_ratios, 'o-', color='#2c3e50')
        plt.xlabel('Number of Tasks')
        plt.ylabel('Feasibility Ratio')
        plt.title('Feasibility Ratio vs Number of Tasks (80% Utilization)')
        plt.grid(True)
        plt.savefig('feasibility_by_tasks.png')
        plt.close()

    def plot_success_rate_by_tasks(self, data):
        """Plot relationship between number of tasks and success rate"""
        task_counts = data['task_counts']
        success_rates = {alg: [] for alg in ['dm', 'edf', 'rr']}
        
        for count in task_counts:
            results = data['results'][str(count)]
            for alg in ['dm', 'edf', 'rr']:
                if results['feasible'] == 0:
                    rate = 0
                else:
                    rate = results[f'{alg}_schedulable'] / results['feasible']
                success_rates[alg].append(rate)
        
        plt.figure(figsize=(10, 6))
        for alg in ['dm', 'edf', 'rr']:
            plt.plot(task_counts, success_rates[alg], 'o-', 
                    label=alg.upper(), color=self.colors[alg])
        
        plt.xlabel('Number of Tasks')
        plt.ylabel('Success Rate')
        plt.title('Success Rate vs Number of Tasks (80% Utilization)')
        plt.legend()
        plt.grid(True)
        plt.savefig('success_rate_by_tasks.png')
        plt.close()

    def plot_feasibility_by_utilization(self, data):
        """Plot relationship between utilization and feasibility ratio"""
        utilizations = data['utilizations']
        feasibility_ratios = []
        
        for util in utilizations:
            results = data['results'][str(util)]
            ratio = results['feasible'] / results['total']
            feasibility_ratios.append(ratio)
            
        plt.figure(figsize=(10, 6))
        plt.plot(utilizations, feasibility_ratios, 'o-', color='#2c3e50')
        plt.xlabel('Utilization (%)')
        plt.ylabel('Feasibility Ratio')
        plt.title('Feasibility Ratio vs Utilization (10 Tasks)')
        plt.grid(True)
        plt.savefig('feasibility_by_utilization.png')
        plt.close()

    def plot_success_rate_by_utilization(self, data):
        """Plot relationship between utilization and success rate"""
        utilizations = data['utilizations']
        success_rates = {alg: [] for alg in ['dm', 'edf', 'rr']}
        
        for util in utilizations:
            results = data['results'][str(util)]
            for alg in ['dm', 'edf', 'rr']:
                if results['feasible'] == 0:
                    rate = 0
                else:
                    rate = results[f'{alg}_schedulable'] / results['feasible']
                success_rates[alg].append(rate)
        
        plt.figure(figsize=(10, 6))
        for alg in ['dm', 'edf', 'rr']:
            plt.plot(utilizations, success_rates[alg], 'o-', 
                    label=alg.upper(), color=self.colors[alg])
        
        plt.xlabel('Utilization (%)')
        plt.ylabel('Success Rate')
        plt.title('Success Rate vs Utilization (10 Tasks)')
        plt.legend()
        plt.grid(True)
        plt.savefig('success_rate_by_utilization.png')
        plt.close()

def plot_results(results_file='analysis_results.json'):
    with open(results_file) as f:
        data = json.load(f)
    
    plotter = Plotter()
    plotter.plot_feasibility_by_tasks(data['task_number_data'])
    plotter.plot_success_rate_by_tasks(data['task_number_data'])
    plotter.plot_feasibility_by_utilization(data['utilization_data'])
    plotter.plot_success_rate_by_utilization(data['utilization_data'])

if __name__ == '__main__':
    plot_results()