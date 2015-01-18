from unittest.case import TestCase
from unittest.mock import patch
import unittest
from os.path import getsize, exists

from database_controller import DatabaseController
import os
from packages.tests.util import TestDirectoryTestCaseMixin


class TestDatabaseController(TestDirectoryTestCaseMixin, TestCase):

    def test_creates_database_on_initialisation(self):
        with patch('models.Base.metadata.create_all') as mock_create_all:
            DatabaseController()

        assert mock_create_all.called, "Controller didn't create database"

    def get_test_db_path(self):
        db_name = 'db.sql'
        path_to_db = os.path.join(self.test_directory, db_name)
        return path_to_db

    def test_creates_database_file_in_path_if_passed(self):
        path_to_db = self.get_test_db_path()

        DatabaseController(path_to_db)
        self.assertTrue(exists(path_to_db))
        self.assertNotEqual(0, getsize(path_to_db))

    def test_creates_engine_using_expected_path_in_sqlite_string(self):

        path_to_db = self.get_test_db_path()
        expected_sql_connection_string = 'sqlite:///%s' % path_to_db

        with patch('sqlalchemy.engine.create_engine') as mock_create_engine:
            DatabaseController(path_to_db)

        mock_create_engine.assert_was_called_with(
            expected_sql_connection_string
        )

    def test_creates_in_memory_engine_by_default(self):

        expected_sql_connection_string = 'sqlite://'

        with patch('sqlalchemy.engine.create_engine') as mock_create_engine:
            DatabaseController()

        mock_create_engine.assert_was_called_with(
            expected_sql_connection_string
        )

    def test_creates_a_session_class_on_initialisation(self):

        controller = DatabaseController()
        self.assertTrue(hasattr(controller, 'Session'))
