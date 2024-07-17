import gitlab
import pandas as pd
from .config_manager import load_config, save_runners_to_config

# Get all runner names from GitLab
def get_all_runner_names(gl, group_id=None, project_id=None):
    all_runners = []

    # Fetch group runners
    if group_id:
        group = gl.groups.get(group_id)
        all_runners.extend(group.runners.list(all=True))

    # Fetch project runners
    if project_id:
        project = gl.projects.get(project_id)
        all_runners.extend(project.runners.list(all=True))

    runner_names = [runner.description for runner in all_runners if runner.description]
    return runner_names

# Fetch all jobs for a project
def fetch_jobs(gl, project_id, status_list=['success'], num_jobs=1000):
    project = gl.projects.get(project_id)
    all_jobs = []
    for status in status_list:
        page = 1
        while len(all_jobs) < num_jobs:
            print(f"Fetching page {page} of jobs with status '{status}'")
            jobs = project.jobs.list(per_page=100, page=page, status=status, get_all=False)
            if not jobs:
                break
            all_jobs.extend(jobs)
            if len(all_jobs) >= num_jobs:
                break
            page += 1
        if len(all_jobs) >= num_jobs:
            break
    all_jobs = all_jobs[:num_jobs]
    print(f"Total jobs fetched: {len(all_jobs)}")
    return all_jobs

# Save jobs to CSV file
def save_jobs_to_csv(jobs, filename):
    jobs_data = []
    for job in jobs:
        if job.runner:  # Adjusted to access the runner attribute
            job_data = {
                'id': job.id,
                'name': job.name,
                'runner_description': job.runner['description'] if job.runner else None,
                'duration': job.duration,
                'created_at': job.created_at,
                'started_at': job.started_at,
                'finished_at': job.finished_at,
                'status': job.status
            }
            jobs_data.append(job_data)
    df = pd.DataFrame(jobs_data)
    df.to_csv(filename, index=False)
    print(f"Jobs saved to {filename}")

def fetch_runners():
    config = load_config()
    gitlab_url = config.get('gitlab', 'url')
    private_token = config.get('gitlab', 'private_token')
    group_id = config.get('gitlab', 'group_id', fallback=None)
    project_id = config.get('gitlab', 'project_id', fallback=None)

    gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
    runner_names = get_all_runner_names(gl, group_id, project_id)
    print(f"Found runners: {runner_names}")
    save_runners_to_config(runner_names)

def fetch_and_save_jobs(output_file):
    config = load_config()
    gitlab_url = config.get('gitlab', 'url')
    private_token = config.get('gitlab', 'private_token')
    project_id = config.get('gitlab', 'project_id')
    num_jobs = config.getint('settings', 'num_jobs', fallback=1000)

    gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
    statuses = ['success', 'failed', 'canceled', 'running']
    jobs = fetch_jobs(gl, project_id, status_list=statuses, num_jobs=num_jobs)
    save_jobs_to_csv(jobs, output_file)
