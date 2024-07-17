import time
import pandas as pd
from config_manager import load_config
from job_processor import load_jobs_from_csv, filter_jobs
from plot_generator import plot_job_durations, plot_comparison

# Parse runners from config
def parse_runners(runners_str):
    return [runner.strip().strip('"') for runner in runners_str.split(',')]

# Function to generate job timing plots
def generate_job_timing_plots(csv_file, graph_runner_names, output_dir):
    config = load_config()
    debug = config.getboolean('settings', 'debug')
    runner_names = parse_runners(config.get('settings', 'runners'))

    if not graph_runner_names:
        graph_runner_names = runner_names

    if len(runner_names) != len(graph_runner_names):
        raise ValueError("The number of runner names and graph runner names must be the same")

    # Load jobs from CSV
    jobs = load_jobs_from_csv(csv_file, debug)

    # Filter jobs for each runner
    start_time = time.time()
    runner_stats = {}
    for runner_name in runner_names:
        runner_stats[runner_name] = filter_jobs(jobs, runner_name, debug)
    end_time = time.time()
    print(f"[DEBUG] Time taken to filter jobs: {end_time - start_time:.2f} seconds.")

    # Log the number of appearances for each job
    all_job_names = set()
    for stats in runner_stats.values():
        all_job_names.update(stats.keys())
    for job in all_job_names:
        appearances = [runner_stats[runner][job][1] if job in runner_stats[runner] else 0 for runner in runner_names]
        print(f"[DEBUG] Job {job} has {appearances} appearances for each runner.")

    # Convert to DataFrame for plotting
    print("[DEBUG] Converting job stats to DataFrames...")
    all_dfs = []
    for runner_name in runner_names:
        df = pd.DataFrame(list(runner_stats[runner_name].items()), columns=['Job', 'Stats'])
        df['Average_Duration'] = df['Stats'].apply(lambda x: x[0])
        df['Appearances'] = df['Stats'].apply(lambda x: x[1])
        df.drop(columns=['Stats'], inplace=True)
        runner_key = runner_name.replace(" ", "_")
        df.rename(columns={'Average_Duration': f'Average_Duration_{runner_key}', 'Appearances': f'Appearances_{runner_key}'}, inplace=True)
        all_dfs.append(df)
    print("[DEBUG] Conversion complete.")

    # Merge and sort DataFrames
    print("[DEBUG] Merging and sorting DataFrames...")
    all_jobs = all_dfs[0]
    for df in all_dfs[1:]:
        all_jobs = pd.merge(all_jobs, df, on='Job', how='outer')
    all_jobs = all_jobs.sort_values(by='Job').fillna(0)

    # Plotting
    print("[DEBUG] Generating plots...")
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta']
    for runner_name, graph_runner_name, color in zip(runner_names, graph_runner_names, colors):
        plot_job_durations(all_jobs, runner_name, graph_runner_name, color, output_dir, print)
    plot_comparison(all_jobs, runner_names, graph_runner_names, output_dir, print)
    print("[DEBUG] Plots generated and saved to files.")
