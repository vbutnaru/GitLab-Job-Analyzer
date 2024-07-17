import os
import matplotlib.pyplot as plt

# Function to plot job durations
def plot_job_durations(all_jobs, runner_name, graph_runner_name, color, output_dir, debug_log):
    os.makedirs(output_dir, exist_ok=True)
    col_name = f'Average_Duration_{runner_name.replace(" ", "_")}'
    output_file = os.path.join(output_dir, f'{runner_name.replace(" ", "_")}_durations.png')
    plt.figure(figsize=(14, 6))
    plt.bar(all_jobs['Job'], all_jobs[col_name], color=color)
    for i, val in enumerate(all_jobs[f'Appearances_{runner_name.replace(" ", "_")}']):
        plt.text(i, all_jobs[col_name][i], f'{all_jobs[col_name][i]:.2f}', ha='center', va='bottom')
    plt.title(f'Job Durations for {graph_runner_name}')
    plt.xlabel('Job Name')
    plt.ylabel('Average Duration (s)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_file)
    debug_log(f"Plot saved to {output_file}", True)
    plt.close()

# Function to plot comparison of job durations
def plot_comparison(all_jobs, runner_names, graph_runner_names, output_dir, debug_log):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'comparison_plot.png')
    plt.figure(figsize=(14, 6))
    width = 0.35
    jobs = all_jobs['Job']
    x = range(len(jobs))
    offsets = [i * width for i in range(len(runner_names))]
    for i, runner_name in enumerate(runner_names):
        col_name = f'Average_Duration_{runner_name.replace(" ", "_")}'
        plt.bar([p + offsets[i] for p in x], all_jobs[col_name], width, label=graph_runner_names[i])
        for j in x:
            plt.text(j + offsets[i], all_jobs[col_name][j], f'{all_jobs[col_name][j]:.2f}', ha='center', va='bottom')
    plt.xticks([p + width * (len(runner_names) - 1) / 2 for p in x], jobs, rotation=90)
    plt.xlabel('Job Name')
    plt.ylabel('Average Duration (s)')
    plt.legend(loc='best')
    plt.title('Comparison of Job Durations')
    plt.tight_layout()
    plt.savefig(output_file)
    debug_log(f"Comparison plot saved to {output_file}", True)
    plt.close()
