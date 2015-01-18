from datetime import datetime, timedelta
from unittest.case import TestCase
from packages.tests.util import DatabaseTestMixin, get_valid_file_reference
from models import FileReference, Snapshot, FileReferenceInSnapshot
from sqlalchemy.exc import IntegrityError


class TestFileReference(DatabaseTestMixin, TestCase):

    def test_table_name_is_underscored(self):
        self.assertEqual('file_reference', FileReference.__tablename__)

    def test_table_has_id(self):
        self.assertTrue(hasattr(FileReference, 'id'))

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


class TestSnapshot(DatabaseTestMixin, TestCase):
    def test_table_name_is_underscored(self):
        self.assertEqual('snapshot', Snapshot.__tablename__)

    def test_table_has_id(self):
        self.assertTrue(hasattr(Snapshot, 'id'))

    def test_datetime_is_set_to_now_by_default(self):
        snapshot = Snapshot()
        self.assertIsNone(snapshot.time)
        self.db_session.add(snapshot)
        self.db_session.flush()

        now = datetime.utcnow()
        a_second_ago = now - timedelta(seconds=1)
        a_second_in_the_future = now + timedelta(seconds=1)
        self.assertGreater(snapshot.time, a_second_ago)
        self.assertGreater(a_second_in_the_future, snapshot.time)


class TestFileReferenceInSnapshot(DatabaseTestMixin, TestCase):

    def test_table_name_is_underscored(self):
        self.assertEqual(
            'file_reference_in_snapshot',
            FileReferenceInSnapshot.__tablename__
        )

    def test_has_reference_to_a_snapshot_and_a_file(self):
        self.assertTrue(hasattr(FileReferenceInSnapshot, "file_reference_id"))
        self.assertTrue(hasattr(FileReferenceInSnapshot, "snapshot_id"))

    def test_can_add_files_to_snapshot_directly(self):
        file_reference = get_valid_file_reference()
        another_file_reference = get_valid_file_reference()

        snapshot = self.add_snapshot_to_database()

        file_reference_in_snapshot = FileReferenceInSnapshot(
            file_reference=file_reference,
            snapshot=snapshot
        )
        another_file_reference_in_snapshot = FileReferenceInSnapshot(
            file_reference=another_file_reference,
            snapshot=snapshot
        )

        self.db_session.add_all(
            [file_reference_in_snapshot, another_file_reference_in_snapshot]
        )
        self.assertEqual(2, self.db_session.query(FileReference).count())
        self.assertEqual(
            2,
            self.db_session.query(FileReferenceInSnapshot).count()
        )

    def add_snapshot_to_database(self):
        snapshot = Snapshot()
        self.db_session.add(snapshot)
        self.db_session.flush()
        return snapshot

    def test_can_add_files_to_snapshot_using_the_snapshot_model(self):
        file_reference = get_valid_file_reference()
        snapshot = self.add_snapshot_to_database()
        snapshot.file_references.append(file_reference)

        self.assertEqual(1, self.db_session.query(FileReference).count())
        self.assertEqual(
            1,
            self.db_session.query(FileReferenceInSnapshot).count()
        )

    def test_can_get_files_in_snapshot_using_the_model(self):

        file_reference = get_valid_file_reference()
        another_file_reference = get_valid_file_reference()

        snapshot = self.add_snapshot_to_database()

        snapshot.file_references.append(file_reference)
        snapshot.file_references.append(another_file_reference)

        self.assertIn(file_reference, snapshot.file_references)
        self.assertIn(another_file_reference, snapshot.file_references)

    def test_deleting_the_snapshot_will_delete_the_associations(self):
        file_reference = get_valid_file_reference()
        another_file_reference = get_valid_file_reference()

        snapshot = self.add_snapshot_to_database()

        snapshot.file_references.append(file_reference)
        snapshot.file_references.append(another_file_reference)

        self.assertEqual(
            2,
            self.db_session.query(FileReferenceInSnapshot).count()
        )

        self.db_session.delete(snapshot)

        self.assertEqual(
            0,
            self.db_session.query(FileReferenceInSnapshot).count()
        )

    def test_deleting_the_snapshot_will_not_delete_the_file_references(self):
        file_reference = get_valid_file_reference()
        another_file_reference = get_valid_file_reference()

        snapshot = self.add_snapshot_to_database()

        snapshot.file_references.append(file_reference)
        snapshot.file_references.append(another_file_reference)

        self.assertEqual(
            2,
            self.db_session.query(FileReference).count()
        )

        self.db_session.delete(snapshot)

        self.assertEqual(
            2,
            self.db_session.query(FileReference).count()
        )

    def test_deleting_the_file_reference_will_delete_the_association(self):
        file_reference = get_valid_file_reference()
        snapshot = self.add_snapshot_to_database()

        snapshot.file_references.append(file_reference)

        self.assertEqual(
            1,
            self.db_session.query(FileReferenceInSnapshot).count()
        )

        self.db_session.delete(file_reference)

        self.assertEqual(
            0,
            self.db_session.query(FileReferenceInSnapshot).count()
        )

    def test_deleting_the_association_wont_delete_snapshot_or_reference(self):
        file_reference = get_valid_file_reference()
        snapshot = self.add_snapshot_to_database()
        file_reference_in_snapshot = FileReferenceInSnapshot(
            file_reference=file_reference,
            snapshot=snapshot
        )

        self.db_session.add(file_reference_in_snapshot)
        self.db_session.flush()
        self.db_session.delete(file_reference_in_snapshot)
        self.assertEqual(1, self.db_session.query(FileReference).count())
        self.assertEqual(1, self.db_session.query(Snapshot).count())
