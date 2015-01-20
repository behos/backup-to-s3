from unittest.case import TestCase
from unittest.mock import patch
from uuid import uuid1

from tests.storage_devices.util import StorageDeviceTestMixin
from tests.util import TempDirectoryTestMixin

from configuration import Configuration
from packages.tests.storage_devices.util import skipIfNotS3
from storage_devices.s3 import S3StorageDevice


@skipIfNotS3
class TestS3StorageDevice(
    TempDirectoryTestMixin,
    StorageDeviceTestMixin,
    TestCase
):

    def get_storage_device(self):
        config = Configuration.get()
        s3_config = config['s3_tests']
        return S3StorageDevice(
            bucket_name=s3_config['bucket_name'],
            access_key_id=s3_config['access_key_id'],
            secret_access_key=s3_config['secret_access_key']
        )

    def test_can_put_file_in_multiparts(self):
        test_path = str(uuid1())

        test_size = 5242880
        chunk_size = int(test_size / 3)
        self.storage_device.chunk_size = chunk_size

        test_file_path = self.create_test_file(test_size)

        with patch(
                'storage_devices.s3.S3StorageDevice._upload_in_chunks'
        ) as mock_upload_in_chunks:
            self.storage_device.put(test_file_path, test_path)

        assert mock_upload_in_chunks.called

    def tearDown(self):
        self._clear_storage_device()
        super(TestS3StorageDevice, self).tearDown()

    def _clear_storage_device(self):
        for key in self.storage_device.list():
            self.storage_device.delete(key)
