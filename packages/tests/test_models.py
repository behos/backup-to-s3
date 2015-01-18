from packages.tests.util import DatabaseTestCase, get_valid_file_reference
from models import FileReference
from sqlalchemy.exc import IntegrityError


class TestFileReference(DatabaseTestCase):

    def test_file_reference_entry_can_be_created(self):

        self.assertEqual(0, self.db_session.query(FileReference).count())
        file_reference = get_valid_file_reference()

        self.db_session.add(file_reference)
        self.assertEqual(1, self.db_session.query(FileReference).count())

    def test_backup_path_is_required_to_add(self):

        file_missing_backup_path = get_valid_file_reference()
        file_missing_backup_path.backup_path = None

        self.assertSaveFailsWithIntegrityError(file_missing_backup_path)

    def test_path_is_required_to_add(self):

        file_missing_path = get_valid_file_reference()
        file_missing_path.path = None

        self.assertSaveFailsWithIntegrityError(file_missing_path)

    def test_hash_is_required_to_add(self):

        file_missing_hash = get_valid_file_reference()
        file_missing_hash.hash = None

        self.assertSaveFailsWithIntegrityError(file_missing_hash)

    def test_backup_path_must_be_unique(self):
        first_file = get_valid_file_reference()
        second_file = get_valid_file_reference()
        second_file.backup_path = first_file.backup_path

        self.db_session.add(first_file)

        self.assertSaveFailsWithIntegrityError(second_file)

    def test_must_have_unique_combination_of_hash_and_path(self):
        first_file = get_valid_file_reference()
        second_file = get_valid_file_reference()
        second_file.path = first_file.path
        second_file.hash = first_file.hash

        self.db_session.add(first_file)
        self.assertSaveFailsWithIntegrityError(second_file)

    def test_can_save_same_path_if_hashes_differ(self):
        self.assertEqual(0, self.db_session.query(FileReference).count())
        first_file = get_valid_file_reference()
        second_file = get_valid_file_reference()
        second_file.path = first_file.path

        self.db_session.add(first_file)
        self.db_session.add(second_file)
        self.assertEqual(2, self.db_session.query(FileReference).count())

    def assertSaveFailsWithIntegrityError(self, object_to_save):

        with self.assertRaises(IntegrityError):
            self.db_session.add(object_to_save)
            self.db_session.flush()
