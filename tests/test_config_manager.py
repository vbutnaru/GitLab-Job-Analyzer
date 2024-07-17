import unittest
import os
from scripts.config_manager import load_config, save_runners_to_config


class TestConfigManager(unittest.TestCase):

    def setUp(self):
        self.test_config_file = 'test_config.ini'
        with open(self.test_config_file, 'w') as f:
            f.write(
                "[gitlab]\nurl = https://gitlab.example.com\nprivate_token = your_private_token\ngroup_id = your_group_id\nproject_id = your_project_id\nrunners = \"on-prem esx vm\",\"gitlab-runner-76\"\n\n[settings]\ndebug = True\nnum_jobs = 10\n")

    def tearDown(self):
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)

    def test_load_config(self):
        config = load_config(self.test_config_file)
        self.assertEqual(config.get('gitlab', 'url'), 'https://gitlab.example.com')

    def test_save_runners_to_config(self):
        save_runners_to_config(['runner1', 'runner2'], self.test_config_file)
        config = load_config(self.test_config_file)
        self.assertEqual(config.get('gitlab', 'runners'), '"runner1","runner2"')


if __name__ == '__main__':
    unittest.main()
