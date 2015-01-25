from uuid import uuid1

import os
from shutil import rmtree
from database.controller import DatabaseController
from database.models import FileReference, Session
from tempfile import mkdtemp, NamedTemporaryFile


class DatabaseTestMixin(object):

    def setUp(self):
        DatabaseController.setup()
        self.db_session = Session()
        super(DatabaseTestMixin, self).setUp()

    def tearDown(self):
        self.db_session.rollback()
        super(DatabaseTestMixin, self).tearDown()


class TempDirectoryTestMixin(object):

    def setUp(self):
        self.test_directory = mkdtemp()
        super(TempDirectoryTestMixin, self).setUp()

    def tearDown(self):
        rmtree(self.test_directory)
        super(TempDirectoryTestMixin, self).tearDown()


class TempFileTestMixin(object):

    def setUp(self):
        self.files_to_delete = []
        super(TempFileTestMixin, self).setUp()

    def create_test_file(self, size=20):
        test_file = NamedTemporaryFile(delete=False)
        self.files_to_delete.append(
            os.path.realpath(test_file.name)
        )

        test_file.truncate(size)
        test_file.close()
        return os.path.realpath(test_file.name)

    def tearDown(self):
        for path in self.files_to_delete:
            os.remove(path)
        super(TempFileTestMixin, self).setUp()


def get_unique_string():
    return str(uuid1())


def get_valid_file_reference():
    return FileReference(
        path=get_unique_string(),
        checksum=get_unique_string(),
        backup_path=get_unique_string()
    )
