import argparse
from runners_fetcher import fetch_runners, fetch_and_save_jobs
from job_timing_main import generate_job_timing_plots

def main():
    parser = argparse.ArgumentParser(description='GitLab Runner and Job Timing Script')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Subcommand to fetch runners
    parser_fetch_runners = subparsers.add_parser('fetch_runners', help='Fetch and save GitLab runners to config file')

    # Subcommand to fetch jobs
    parser_fetch_jobs = subparsers.add_parser('fetch_jobs', help='Fetch and save GitLab jobs to CSV file')
    parser_fetch_jobs.add_argument('--output_file', type=str, required=True, help='Path to the output CSV file')

    # Subcommand to generate job timing plots
    parser_generate_plots = subparsers.add_parser('generate_plots', help='Generate job timing plots')
    parser_generate_plots.add_argument('--csv_file', type=str, required=True, help='Path to the CSV file containing jobs')
    parser_generate_plots.add_argument('--graph_runner_names', type=str, nargs='+', help='Display names of the runners on graphs')
    parser_generate_plots.add_argument('--output_dir', type=str, default='comparison-png', help='Directory to save the output images')

    args = parser.parse_args()

    if args.command == 'fetch_runners':
        fetch_runners()
    elif args.command == 'fetch_jobs':
        fetch_and_save_jobs(args.output_file)
    elif args.command == 'generate_plots':
        generate_job_timing_plots(args.csv_file, args.graph_runner_names, args.output_dir)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
