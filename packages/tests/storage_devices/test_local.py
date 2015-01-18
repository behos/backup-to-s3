from unittest.case import TestCase
import os
from packages.tests.storage_devices.util import StorageDeviceTestMixin
from packages.tests.util import TestDirectoryTestCaseMixin
from storage_devices.exceptions import StorageDeviceError
from storage_devices.local import LocalStorageDevice


class TestLocalStorageDevice(
    TestDirectoryTestCaseMixin,
    StorageDeviceTestMixin,
    TestCase
):

    def get_storage_device(self):
        return LocalStorageDevice(self.test_directory)

    def test_cannot_get_file_to_path_in_storage_device(self):

        expected_file, expected_size, expected_path = \
            self.put_file_to_storage_device()

        with self.assertRaises(StorageDeviceError):
            self.storage_device.get(
                expected_path,
                os.path.join(self.test_directory, expected_path)
            )

    def test_cannot_put_file_with_path_in_storage_device(self):

        with self.assertRaises(StorageDeviceError):
            self.storage_device.put(
                os.path.join(self.test_directory, 'path'),
                'other path'
            )

    def test_cannot_put_file_in_subfolder_if_conflict_with_other_path(self):
        self.put_file_to_storage_device(os.path.join('file', 'in'))

        with self.assertRaises(NotADirectoryError):
            self.put_file_to_storage_device(
                os.path.join('file', 'in', 'folder')
            )
