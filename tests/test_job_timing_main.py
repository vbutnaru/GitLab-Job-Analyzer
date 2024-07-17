import unittest
from unittest.mock import patch, MagicMock, ANY
from scripts.job_timing_main import generate_job_timing_plots

class TestJobTimingMain(unittest.TestCase):

    @patch('scripts.job_timing_main.load_config')
    @patch('scripts.job_timing_main.load_jobs_from_csv')
    @patch('scripts.job_timing_main.filter_jobs')
    @patch('scripts.job_timing_main.plot_job_durations')
    @patch('scripts.job_timing_main.plot_comparison')
    def test_generate_job_timing_plots(self, mock_plot_comparison, mock_plot_durations, mock_filter_jobs, mock_load_jobs, mock_load_config):
        mock_config = MagicMock()
        mock_config.getboolean.return_value = True
        mock_config.get.return_value = '"runner1","runner2"'
        mock_load_config.return_value = mock_config

        mock_load_jobs.return_value = [
            {'id': 1, 'name': 'job1', 'runner': {'description': 'runner1'}, 'duration': 10},
            {'id': 2, 'name': 'job2', 'runner': {'description': 'runner2'}, 'duration': 20}
        ]
        mock_filter_jobs.return_value = {
            'job1': (10, 1),
            'job2': (20, 1)
        }

        generate_job_timing_plots('test_jobs.csv', ['Runner 1', 'Runner 2'], 'output_dir')

        mock_load_jobs.assert_called_once_with('test_jobs.csv', True)
        mock_filter_jobs.assert_any_call(mock_load_jobs.return_value, 'runner1', True)
        mock_filter_jobs.assert_any_call(mock_load_jobs.return_value, 'runner2', True)
        mock_plot_durations.assert_any_call(ANY, 'runner1', 'Runner 1', 'blue', 'output_dir', print)
        mock_plot_durations.assert_any_call(ANY, 'runner2', 'Runner 2', 'green', 'output_dir', print)
        mock_plot_comparison.assert_called_once()

if __name__ == '__main__':
    unittest.main()
