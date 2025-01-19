import csv

def parse_taskset(file_path):
    tasks = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            O, C, D, T = map(int, row)
            tasks.append({'O': O, 'C': C, 'D': D, 'T': T})
    return tasks