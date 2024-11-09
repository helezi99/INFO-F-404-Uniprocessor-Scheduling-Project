# src/task.py
class Task:
    def __init__(self, offset, computation_time, deadline, period):
        self.offset = offset
        self.computation_time = computation_time
        self.deadline = deadline
        self.period = period
        
        # Additional attributes for EDF scheduling
        self.remaining_time = 0  # Remaining execution time
        self.next_deadline = 0   # Next absolute deadline
        self.next_release = 0    # Next release time
        
    def get_absolute_deadline(self, current_time):
        """Calculate the absolute deadline of the current job"""
        if current_time < self.offset:
            return self.offset + self.deadline
        return self.offset + ((current_time - self.offset) // self.period) * self.period + self.deadline

    def is_ready(self, current_time):
        """Check if the task is ready"""
        return current_time >= self.next_release
    

class TaskSet:
    def __init__(self, tasks):
        self.tasks = tasks

    @classmethod
    def from_file(cls, filepath):
        """
        Read task set from CSV file
        File format: each line contains offset,computation_time,deadline,period
        
        Args:
            filepath: Path to the task set file
            
        Returns:
            TaskSet: A TaskSet object containing all tasks
            
        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file format is invalid
        """
        tasks = []
        
        try:
            with open(filepath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    # Remove whitespace and split
                    values = line.strip().split(',')
                    
                    # Check if we have the correct number of values
                    if len(values) != 4:
                        raise ValueError(f"Line {line_num}: Expected 4 values, got {len(values)}")
                    
                    try:
                        # Convert to integers
                        offset, comp_time, deadline, period = map(int, values)
                        
                        # Validate values
                        if comp_time <= 0:
                            raise ValueError(f"Line {line_num}: Computation time must be positive")
                        if deadline <= 0:
                            raise ValueError(f"Line {line_num}: Deadline must be positive")
                        if period <= 0:
                            raise ValueError(f"Line {line_num}: Period must be positive")
                        if offset < 0:
                            raise ValueError(f"Line {line_num}: Offset must be non-negative")
                        
                        # Create Task object
                        task = Task(offset, comp_time, deadline, period)
                        tasks.append(task)
                        
                    except ValueError as e:
                        if str(e).startswith("Line"):
                            raise
                        raise ValueError(f"Line {line_num}: Invalid number format")
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"Task set file not found: {filepath}")
            
        if not tasks:
            raise ValueError("Task set file is empty")
            
        return cls(tasks)

    def __len__(self):
        return len(self.tasks)

    def __getitem__(self, index):
        return self.tasks[index]

    def __iter__(self):
        return iter(self.tasks)