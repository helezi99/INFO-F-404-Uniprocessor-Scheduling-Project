# Multiprocessor Scheduling Project

## Overview
This project implements multiprocessor scheduling algorithms (Partitioned and Global EDF) for task sets with arbitrary deadlines.

## Directory Structure
- **tasksets/**: Contains CSV files with task set data.
- **src/**: Contains the Python implementation of the project.
- **results/**: Stores outputs such as schedulability reports.

## Usage
Run the program using:
```bash
python main.py <task_file> <m> -v <version> [-w <workers>] [-h <heuristic>] [-s <sort_order>]
