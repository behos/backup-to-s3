from unittest.case import TestCase
import datetime
from database_controller import DatabaseController
from models import BackedUpFile


class DatabaseTestCase(TestCase):

    def setUp(self):
        self.db_session = DatabaseController().get_session()

    def tearDown(self):
        self.db_session.rollback()


def get_valid_backed_up_file():
    return BackedUpFile(
        path="a_path",
        last_backed_up_on=datetime.datetime.now(),
        last_backed_up_hash="a file hash"
    )
