from models import Snapshot, FileReference
from os import makedirs
import os
from unittest.case import TestCase
from tests.util import DatabaseTestMixin
from packages.tests.util import TempFileTestMixin, TempDirectoryTestMixin
from snapshot.snapshot_taker import SnapshotTaker
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
