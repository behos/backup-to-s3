from unittest.case import TestCase
from unittest.mock import patch
from database.models import Snapshot, FileReference
from os import makedirs
from packages.tests.util import DatabaseTestMixin, TempDirectoryTestMixin, \
    TempFileTestMixin
from snapshot.restorer import SnapshotRestorer
from storage_devices.local import LocalStorageDevice
import os


class TestSnapshotRestorer(
    DatabaseTestMixin,
    TempDirectoryTestMixin,
    TempFileTestMixin,
    TestCase
):
    def setUp(self):
        super(TestSnapshotRestorer, self).setUp()

        source_directory = os.path.join(self.test_directory, "backups")
        destination_directory = os.path.join(
            self.test_directory,
            "restore"
        )

        makedirs(source_directory)
        makedirs(destination_directory)

        self.source_storage_device = LocalStorageDevice(source_directory)
        self.destination_storage_device = LocalStorageDevice(
            destination_directory
        )

        self.snapshot_restorer = SnapshotRestorer(
            self.source_storage_device,
            self.destination_storage_device
        )

    def test_restorer_restores_files_from_snapshots(self):
        snapshot, file_reference, path = self._create_snapshot_with_test_file()
        self.snapshot_restorer.restore_snapshot(snapshot)

        self.assertFileInDestination(file_reference, path)

    def test_restores_files_from_snapshots_if_different_checksum(self):
        snapshot, file_reference, path = self._create_snapshot_with_test_file()

        different_test_file = self.create_test_file()
        self.destination_storage_device.put(different_test_file, path)

        self.assertNotEqual(
            file_reference.checksum,
            self.destination_storage_device.checksum(path)
        )

        self.snapshot_restorer.restore_snapshot(snapshot)

        self.assertFileInDestination(file_reference, path)

    def test_does_not_restore_files_if_they_exist(self):
        snapshot, file_reference, path = self._create_snapshot_with_test_file()

        test_file_path = self.create_test_file(0)
        self.source_storage_device.get(
            path,
            test_file_path
        )

        self.destination_storage_device.put(test_file_path, path)
        self.assertEqual(
            file_reference.checksum,
            self.source_storage_device.checksum(path)
        )

        self.assertFileInDestination(file_reference, path)

        with patch('snapshot.restorer.SnapshotRestorer._restore_file') \
                as patched_restore_file:
            self.snapshot_restorer.restore_snapshot(snapshot)

        assert not patched_restore_file.called

    def _create_snapshot_with_test_file(self):
        snapshot = Snapshot()
        self.db_session.add(snapshot)
        test_size = 100
        file_path = self.create_test_file(test_size)
        path = "testfile"

        file_reference = self._put_file_in_backups(
            file_path,
            path
        )

        snapshot.file_references.append(file_reference)
        return snapshot, file_reference, path

    def _put_file_in_backups(self, file_path, name_in_storage_device):
        self.source_storage_device.put(file_path, name_in_storage_device)
        checksum = self.source_storage_device.checksum(name_in_storage_device)
        file_reference = FileReference(
            path=name_in_storage_device,
            backup_path=name_in_storage_device,
            checksum=checksum
        )

        return file_reference

    def assertFileInDestination(self, file_reference, name_in_storage_device):
        all_files_in_destination = self.destination_storage_device.list()
        self.assertEqual(1, len(all_files_in_destination))

        self.assertTrue(
            self.destination_storage_device.exists(name_in_storage_device)
        )

        self.assertEqual(
            file_reference.checksum,
            self.destination_storage_device.checksum(name_in_storage_device)
        )
