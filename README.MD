# Uniprocessor Scheduling Project

**INFO-F-404: Real-Time Operating Systems (2024/25) - ULB**  
Work: Herma Elezi , Zexin Zhang

<div align="center">
    <img src="https://actus.ulb.be/medias/photo/logo-universite-libre-bruxelles_1661952138925-png?ID_FICHE=19524" alt="ULB Logo" width="300"/>
</div>

## Introduction

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
