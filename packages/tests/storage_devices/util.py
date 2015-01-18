from unittest.case import TestCase
from packages.tests.util import TestDirectoryTestCaseMixin


class StorageDeviceTestCase(TestDirectoryTestCaseMixin, TestCase):

    def setUp(self):
        super(StorageDeviceTestCase, self).setUp()
        self.storage_device = self.storage_device_class()

    def test_can_put_file_to_storage_device(self):
        pass
