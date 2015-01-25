from unittest.case import TestCase

from tests.util import DatabaseTestMixin

from database.models import Snapshot, FileReference
from os import makedirs
import os
from packages.tests.util import TempFileTestMixin, TempDirectoryTestMixin
from snapshot.taker import SnapshotTaker
from storage_devices.local import LocalStorageDevice


class TestSnapshotTaker(
    DatabaseTestMixin,
    TempDirectoryTestMixin,
    TempFileTestMixin,
    TestCase
):
    def setUp(self):
        super(TestSnapshotTaker, self).setUp()

        source_directory = os.path.join(self.test_directory, "source")
        destination_directory = os.path.join(
            self.test_directory,
            "destination"
        )

        makedirs(source_directory)
        makedirs(destination_directory)

        self.source_storage_device = LocalStorageDevice(source_directory)
        self.destination_storage_device = LocalStorageDevice(
            destination_directory
        )

        self.snapshot_taker = SnapshotTaker(
            self.source_storage_device,
            self.destination_storage_device
        )

    def test_take_snapshot_transfers_files_to_destination_storage_device(self):
        test_size = 100
        file_path = self.create_test_file(test_size)
        name_in_storage_device = "testfile"
        self.source_storage_device.put(file_path, name_in_storage_device)

        self.snapshot_taker.take_snapshot()

        all_files_in_destination = self.destination_storage_device.list()
        self.assertEqual(1, len(all_files_in_destination))

    def test_take_snapshot_suffixes_files_to_destination_storage_device(self):
        test_size = 100
        file_path = self.create_test_file(test_size)
        name_in_storage_device = "testfile"
        self.source_storage_device.put(file_path, name_in_storage_device)

        self.snapshot_taker.take_snapshot()

        all_files_in_destination = self.destination_storage_device.list()
        transferred_file = all_files_in_destination[0]

        self.assertNotEqual(
            name_in_storage_device,
            transferred_file
        )

        self.assertTrue(
            transferred_file.startswith(name_in_storage_device)
        )

    def test_take_snapshot_creates_a_snapshot_object_in_the_database(self):
        self.assertEqual(0, self.db_session.query(Snapshot).count())
        self.snapshot_taker.take_snapshot()
        self.assertEqual(1, self.db_session.query(Snapshot).count())

    def test_take_snapshot_adds_references_to_all_files_in_the_snapshot(self):
        file_path = self.create_test_file()
        path_1 = "testfile-1"
        path_2 = "testfile-2"

        self.source_storage_device.put(file_path, path_1)
        self.source_storage_device.put(file_path, path_2)

        self.assertEqual(0, self.db_session.query(FileReference).count())
        self.snapshot_taker.take_snapshot()
        self.assertEqual(2, self.db_session.query(FileReference).count())
        snapshot = self.db_session.query(Snapshot).first()
        self.assertEqual(path_1, snapshot.file_references[0].path)
        self.assertEqual(path_2, snapshot.file_references[1].path)

    def test_take_snapshot_does_not_add_file_reference_if_unchanged(self):
        file_path = self.create_test_file()
        path = "testfile"

        self.source_storage_device.put(file_path, path)

        self.assertEqual(0, self.db_session.query(FileReference).count())
        self.snapshot_taker.take_snapshot()
        self.snapshot_taker.take_snapshot()
        self.snapshot_taker.take_snapshot()
        self.snapshot_taker.take_snapshot()

        self.assertEqual(4, self.db_session.query(Snapshot).count())
        self.assertEqual(1, self.db_session.query(FileReference).count())

        for snapshot in self.db_session.query(Snapshot).all():
            self.assertEqual(path, snapshot.file_references[0].path)

    def test_take_snapshot_adds_new_file_reference_if_changed(self):
        file_path = self.create_test_file(size=10)
        path = "testfile"

        self.source_storage_device.put(file_path, path)

        self.assertEqual(0, self.db_session.query(FileReference).count())
        self.snapshot_taker.take_snapshot()

        file_path = self.create_test_file(size=12)

        self.source_storage_device.delete(path)
        self.source_storage_device.put(file_path, path)

        self.snapshot_taker.take_snapshot()

        self.assertEqual(2, self.db_session.query(Snapshot).count())
        self.assertEqual(2, self.db_session.query(FileReference).count())

        for snapshot in self.db_session.query(Snapshot).all():
            self.assertEqual(path, snapshot.file_references[0].path)
