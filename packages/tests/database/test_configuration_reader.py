from unittest.case import TestCase
from unittest.mock import patch
from database.configuration_reader import DatabaseConfigurationReader
from snapshot.exceptions import InvalidConfigurationError


class TestDatabaseConfigurationReader(TestCase):

    def test_raises_error_if_not_configured(self):

        configuration = {}

        with patch('configuration.Configuration.get',
                   return_value=configuration):
            with self.assertRaises(InvalidConfigurationError):
                DatabaseConfigurationReader.get_path()

    def test_returns_configured_path(self):

        configuration = {
            'database_path': 'path'
        }

        with patch('configuration.Configuration.get',
                   return_value=configuration):
            self.assertEqual('path', DatabaseConfigurationReader.get_path())
