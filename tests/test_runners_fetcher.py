import unittest
from unittest.mock import patch, MagicMock
from scripts.runners_fetcher import fetch_jobs, save_jobs_to_csv, fetch_runners, fetch_and_save_jobs

class TestRunnersFetcher(unittest.TestCase):

    @patch('scripts.runners_fetcher.gitlab.Gitlab')
    def test_fetch_jobs(self, MockGitlab):
        mock_gl = MockGitlab.return_value
        mock_project = mock_gl.projects.get.return_value
        mock_job = MagicMock()
        mock_job.status = 'success'
        mock_job.runner = {'description': 'runner1'}
        mock_project.jobs.list.return_value = [mock_job] * 100

        jobs = fetch_jobs(mock_gl, 'project_id', status_list=['success'], num_jobs=100)
        self.assertEqual(len(jobs), 100)

    @patch('scripts.runners_fetcher.pd.DataFrame.to_csv')
    def test_save_jobs_to_csv(self, mock_to_csv):
        jobs = [
            MagicMock(id=1, name='job1', runner={'description': 'runner1'}, duration=10, created_at='2023-07-17T00:00:00Z', started_at='2023-07-17T00:00:00Z', finished_at='2023-07-17T00:00:00Z', status='success')
        ]
        save_jobs_to_csv(jobs, 'test_jobs.csv')
        mock_to_csv.assert_called_once()

    @patch('scripts.runners_fetcher.get_all_runner_names', return_value=['runner1', 'runner2'])
    @patch('scripts.runners_fetcher.save_runners_to_config')
    @patch('scripts.runners_fetcher.load_config')
    def test_fetch_runners(self, mock_load_config, mock_save_runners, mock_get_all_runners):
        fetch_runners()
        mock_get_all_runners.assert_called_once()
        mock_save_runners.assert_called_once_with(['runner1', 'runner2'])

    @patch('scripts.runners_fetcher.fetch_jobs', return_value=[MagicMock(id=1, name='job1', runner={'description': 'runner1'}, duration=10, created_at='2023-07-17T00:00:00Z', started_at='2023-07-17T00:00:00Z', finished_at='2023-07-17T00:00:00Z', status='success')])
    @patch('scripts.runners_fetcher.save_jobs_to_csv')
    @patch('scripts.runners_fetcher.load_config')
    def test_fetch_and_save_jobs(self, mock_load_config, mock_save_jobs, mock_fetch_jobs):
        fetch_and_save_jobs('test_jobs.csv')
        mock_fetch_jobs.assert_called_once()
        mock_save_jobs.assert_called_once()

if __name__ == '__main__':
    unittest.main()
