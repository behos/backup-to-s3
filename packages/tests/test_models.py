from packages.tests.util import DatabaseTestCase, get_valid_backed_up_file
from models import BackedUpFile
from sqlalchemy.exc import IntegrityError


class TestBackedUpFile(DatabaseTestCase):

    def test_backed_up_file_entry_can_be_created(self):

        session = self.db_session
        self.assertEqual(0, session.query(BackedUpFile).count())
        backed_up_file = get_valid_backed_up_file()

        session.add(backed_up_file)
        self.assertEqual(1, session.query(BackedUpFile).count())

    def test_date_is_required_to_add(self):

        backed_up_file_missing_date = get_valid_backed_up_file()
        backed_up_file_missing_date.last_backed_up_on = None

        self.assertSaveFailsWithIntegrityError(backed_up_file_missing_date)

    def test_path_is_required_to_add(self):

        backed_up_file_missing_path = get_valid_backed_up_file()
        backed_up_file_missing_path.path = None

        self.assertSaveFailsWithIntegrityError(backed_up_file_missing_path)

    def test_hash_is_required_to_add(self):

        backed_up_file_missing_hash = get_valid_backed_up_file()
        backed_up_file_missing_hash.last_backed_up_hash = None

        self.assertSaveFailsWithIntegrityError(backed_up_file_missing_hash)

    def assertSaveFailsWithIntegrityError(self, object_to_save):

        with self.assertRaises(IntegrityError):
            self.db_session.add(object_to_save)
            self.db_session.flush()
