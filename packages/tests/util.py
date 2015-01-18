from uuid import uuid1
from shutil import rmtree
from database_controller import DatabaseController
from models import FileReference
from tempfile import mkdtemp


class DatabaseTestMixin(object):

    def setUp(self):
        self.db_session = DatabaseController().get_session()
        super(DatabaseTestMixin, self).setUp()

    def tearDown(self):
        self.db_session.rollback()
        super(DatabaseTestMixin, self).tearDown()


class TestDirectoryTestCaseMixin(object):

    def setUp(self):
        self.test_directory = mkdtemp()
        super(TestDirectoryTestCaseMixin, self).setUp()

    def tearDown(self):
        rmtree(self.test_directory)
        super(TestDirectoryTestCaseMixin, self).tearDown()


def get_unique_string():
    return str(uuid1())


def get_valid_file_reference():
    return FileReference(
        path=get_unique_string(),
        hash=get_unique_string(),
        backup_path=get_unique_string()
    )
