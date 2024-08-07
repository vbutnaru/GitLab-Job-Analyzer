import pandas as pd
from collections import defaultdict

# Debug function
def debug_log(message, debug):
    if debug:
        print(f"[DEBUG] {message}")

# Function to load jobs from CSV

def load_jobs_from_csv(filename, debug):
    if debug:
        print(f"[DEBUG] Loading jobs from {filename}...")
    df = pd.read_csv(filename)
    if debug:
        print(f"[DEBUG] DataFrame loaded:\n{df}")
    jobs = []
    for index, row in df.iterrows():
        if debug:
            print(f"[DEBUG] Processing row: {row.to_dict()}")
        if row['runner_description'] and row['duration']:
            job = {
                'id': row['id'],
                'name': row['name'],
                'runner': {'description': row['runner_description']} if row['runner_description'] else None,
                'duration': row['duration']
            }
            jobs.append(job)
    if debug:
        print(f"[DEBUG] Loaded {len(jobs)} jobs from {filename}.")
    return jobs



# Function to filter jobs by runner and calculate average duration and appearances
def filter_jobs(jobs, runner_name, debug):
    debug_log(f"Filtering jobs for runner: {runner_name}...", debug)
    runner_jobs = defaultdict(list)
    for job in jobs:
        if job['runner']:
            job_runner_desc = job['runner']['description']
            job_name = job['name']
            job_duration = job['duration']

            if job_runner_desc == runner_name:
                runner_jobs[job_name].append(job_duration)

    job_stats = {job: (sum(durations) / len(durations), len(durations)) for job, durations in runner_jobs.items()}
    return job_stats
