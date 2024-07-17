import unittest
from unittest.mock import patch
from scripts.job_processor import load_jobs_from_csv, filter_jobs
import pandas as pd
from io import StringIO


class TestJobProcessor(unittest.TestCase):

    @patch('scripts.job_processor.pd.read_csv')
    def test_load_jobs_from_csv(self, mock_read_csv):
        # Mock DataFrame setup
        data = """id,name,runner_description,duration
1,job1,runner1,10
2,job2,runner2,20"""
        df = pd.read_csv(StringIO(data))
        mock_read_csv.return_value = df

        # Debug output to verify the DataFrame content
        print(f"[DEBUG] DataFrame for mocking:\n{df}")

        jobs = load_jobs_from_csv('test_jobs.csv', debug=True)

        # Debug output to verify jobs loaded
        print(f"[DEBUG] Jobs loaded: {jobs}")

        # Ensure DataFrame content is correctly returned by the mock
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['id'], 1)
        self.assertEqual(df.iloc[1]['duration'], 20)

        # Ensure jobs are loaded correctly
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]['id'], 1)
        self.assertEqual(jobs[1]['duration'], 20)

    def test_filter_jobs(self):
        jobs = [
            {'id': 1, 'name': 'job1', 'runner': {'description': 'runner1'}, 'duration': 10},
            {'id': 2, 'name': 'job2', 'runner': {'description': 'runner1'}, 'duration': 20},
            {'id': 3, 'name': 'job3', 'runner': {'description': 'runner2'}, 'duration': 30}
        ]
        runner_stats = filter_jobs(jobs, 'runner1', debug=True)
        self.assertEqual(len(runner_stats), 2)
        self.assertEqual(runner_stats['job1'][0], 10)
        self.assertEqual(runner_stats['job2'][1], 1)


if __name__ == '__main__':
    unittest.main()
