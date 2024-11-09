# Uniprocessor Scheduling Project

**INFO-F-404: Real-Time Operating Systems (2024/25) - ULB**  
Work: Herma Elezi , Zexin Zhang

![ULB Logo](https://camo.githubusercontent.com/347eaad2540c5565afffac408a52ca9cbf077a574f201fe970c131b6044ea177/68747470733a2f2f61637475732e756c622e62652f6d65646961732f70686f746f2f6c6f676f2d756e69766572736974652d6c696272652d62727578656c6c65735f313636313935323133383932352d706e673f49445f46494348453d3139353234)

This project is part of the Real-Time Operating Systems course at the Department of Computer Science, Faculté des Sciences. The goal is to simulate uniprocessor scheduling for synchronous task sets with constrained deadlines using three priority assignment algorithms: Deadline Monotonic (DM), Earliest Deadline First (EDF), and Round Robin (RR). The project also includes a report comparing the performance of these algorithms.


## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command-line Arguments

To run the scheduler, use the following command:
```bash
python main.py <algorithm> <taskset_file> [-v]
