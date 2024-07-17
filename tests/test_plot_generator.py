import unittest
from unittest.mock import patch
from scripts.plot_generator import plot_job_durations, plot_comparison
import pandas as pd

class TestPlotGenerator(unittest.TestCase):

    @patch('scripts.plot_generator.plt.savefig')
    def test_plot_job_durations(self, mock_savefig):
        data = {
            'Job': ['job1', 'job2'],
            'Average_Duration_runner1': [10, 20],
            'Appearances_runner1': [1, 2]
        }
        df = pd.DataFrame(data)
        plot_job_durations(df, 'runner1', 'Runner 1', 'blue', 'output_dir', print)
        mock_savefig.assert_called_once()

    @patch('scripts.plot_generator.plt.savefig')
    def test_plot_comparison(self, mock_savefig):
        data = {
            'Job': ['job1', 'job2'],
            'Average_Duration_runner1': [10, 20],
            'Appearances_runner1': [1, 2],
            'Average_Duration_runner2': [15, 25],
            'Appearances_runner2': [1, 1]
        }
        df = pd.DataFrame(data)
        plot_comparison(df, ['runner1', 'runner2'], ['Runner 1', 'Runner 2'], 'output_dir', print)
        mock_savefig.assert_called_once()

if __name__ == '__main__':
    unittest.main()
