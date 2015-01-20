from unittest.case import skipUnless
from uuid import uuid1

from configuration import Configuration
from packages.tests.util import TempFileTestMixin
from random import randint
from tempfile import NamedTemporaryFile
import os


class StorageDeviceTestMixin(TempFileTestMixin):

    def setUp(self):
        self.storage_device = self.get_storage_device()
        super(StorageDeviceTestMixin, self).setUp()

    def get_storage_device(self):
        raise NotImplementedError()

    def test_can_put_file(self):
        test_file, expected_size, expected_path = \
            self.put_file_to_storage_device()

        self.assertTrue(
            self.storage_device.exists(expected_path)
        )

        self.assertEqual(
            expected_size, self.storage_device.size(expected_path)
        )

    def put_file_to_storage_device(self, test_path=None):
        if not test_path:
            test_path = str(uuid1())

        test_size = randint(2, 19)
        test_file_path = self.create_test_file(test_size)
        self.storage_device.put(test_file_path, test_path)
        return test_file_path, test_size, test_path

    def test_can_put_file_in_subfolder(self):
        test_file, expected_size, expected_path = \
            self.put_file_to_storage_device(
                os.path.join('file', 'in', 'folder')
            )

        self.assertTrue(
            self.storage_device.exists(expected_path)
        )

        self.assertEqual(
            expected_size, self.storage_device.size(expected_path)
        )

    def test_can_get_file(self):
        test_file_path, expected_size, expected_path = \
            self.put_file_to_storage_device()

        destination_path = os.path.abspath(NamedTemporaryFile().name)
        self.storage_device.get(expected_path, destination_path)
        with open(destination_path) as retrieved_file, \
                open(test_file_path) as test_file:

            self.assertEqual(test_file.read(), retrieved_file.read())

    def test_can_delete_file(self):
        expected_file, expected_size, expected_path = \
            self.put_file_to_storage_device()

        self.assertTrue(self.storage_device.exists(expected_path))
        self.storage_device.delete(expected_path)
        self.assertFalse(self.storage_device.exists(expected_path))

    def test_raises_not_found_error_when_trying_to_get_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.storage_device.get('non existant path', 'some other path')

    def test_raises_not_found_error_when_trying_to_delete_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.storage_device.delete('non existant path')

    def test_can_get_file_size(self):
        expected_file, expected_size, expected_path = \
            self.put_file_to_storage_device()

        self.assertEqual(
            expected_size,
            self.storage_device.size(expected_path)
        )

    def test_list_gets_all_file_paths(self):
        expected_file, expected_size, expected_path = \
            self.put_file_to_storage_device()

        expected_file, expected_size, other_expected_path = \
            self.put_file_to_storage_device(
                os.path.join('file', 'in', 'folder')
            )

        file_list = self.storage_device.list()

        self.assertTrue(
            all(
                path in file_list
                for path in [
                    expected_path,
                    other_expected_path
                ]
            )
        )

    def test_raises_file_exists_error_when_putting_file_in_existing(self):
        expected_file, expected_size, expected_path = \
            self.put_file_to_storage_device()

        with self.assertRaises(FileExistsError):
            self.storage_device.put(expected_file, expected_path)


skipIfNotS3 = skipUnless(
    's3_tests' in Configuration.get(),
    'Skipping S3 tests because no configuration exists'
)
