
import unittest
from unittest.mock import patch, MagicMock
import main

class TestMain(unittest.TestCase):
    @patch('main.subprocess.run')
    def test_run_checks_linux(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='[{"check": "Password Policy", "status": "Compliant", "details": "minlen set to 12"}]')
        custom_rules = {"password_policy": {"minlen": 12}}
        result = main.run_checks('Linux', custom_rules)
        self.assertIsNotNone(result)
        self.assertEqual(result[0]['check'], 'Password Policy')

    @patch('main.subprocess.run')
    def test_run_checks_windows(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='[{"check": "Password Policy", "status": "Compliant", "details": "Minimum length set to 12 characters."}]')
        custom_rules = {"password_policy": {"minPasswordLength": 12}}
        result = main.run_checks('Windows', custom_rules)
        self.assertIsNotNone(result)
        self.assertEqual(result[0]['check'], 'Password Policy')

if __name__ == '__main__':
    unittest.main()