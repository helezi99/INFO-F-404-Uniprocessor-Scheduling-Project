import os
import argparse
import time
from multiprocessing import Pool
from utils.parser import parse_taskset
from scheduler.partitioned import partitioned_edf
from scheduler.global_ import global_edf
from scheduler.edf_k import edf_k
from utils.schedulability import determine_schedulability
import json

def process_taskset(task_file, args):
    start_time = time.time()

    tasks = parse_taskset(task_file)
    if args.version == "partitioned":
        result = partitioned_edf(tasks, args.m, args.heuristic, args.sort)
    elif args.version == "global":
        result = global_edf(tasks, args.m)
    elif args.version == "k":
        result = edf_k(tasks, args.m, k=2)

    schedulability_code = determine_schedulability(tasks, args.m, interval=(0, 100))
    end_time = time.time()
    processing_time = end_time - start_time

    return {
        "taskset": task_file,
        "scheduling_result": result,
        "schedulability_code": schedulability_code,
        "processing_time": processing_time
    }

def main():
    parser = argparse.ArgumentParser(description="Multiprocessor Scheduling Tool")
    parser.add_argument("tasksets_dir", help="Path to the directory containing task set files")
    parser.add_argument("m", type=int, help="Number of cores")
    parser.add_argument("-v", "--version", choices=["global", "partitioned", "k"], required=True)
    parser.add_argument("-H", "--heuristic", choices=["ff", "nf", "bf", "wf"], default="ff",
                        help="Heuristic to use for partitioned scheduling")
    parser.add_argument("-s", "--sort", choices=["iu", "du"], default="iu",
                        help="Task sorting order for partitioning")
    parser.add_argument("-o", "--output", help="Output file to save results", default="performance_results.json")
    args = parser.parse_args()

    # Ensure the tasksets directory exists
    if not os.path.isdir(args.tasksets_dir):
        print(f"Error: {args.tasksets_dir} is not a directory.")
        return

    taskset_files = [os.path.join(args.tasksets_dir, f) for f in os.listdir(args.tasksets_dir) if f.startswith("taskset")]

    # Measure performance for worker counts from 1 to 32
    performance_results = []
    for worker_count in range(1, 33):
        start_time = time.time()

        # Process all tasksets with the current number of workers
        with Pool(processes=worker_count) as pool:
            pool.starmap(process_taskset, [(task_file, args) for task_file in taskset_files])

        end_time = time.time()
        total_processing_time = end_time - start_time

        performance_results.append({
            "worker_count": worker_count,
            "total_processing_time": total_processing_time
        })

        print(f"Worker Count: {worker_count}, Total Processing Time: {total_processing_time:.4f} seconds")

    # Save performance results to a file
    if args.output:
        with open(args.output, "w") as outfile:
            json.dump(performance_results, outfile, indent=4)
        print(f"Performance results saved to {args.output}")

if __name__ == "__main__":
    main()
