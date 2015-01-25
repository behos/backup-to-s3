from unittest.case import TestCase
from unittest.mock import patch
from snapshot.configruation_reader import SnapshotConfigurationReader
from snapshot.exceptions import InvalidConfigurationError
from storage_devices.local import LocalStorageDevice


class TestSnapshotController(TestCase):

    valid_local_configuration = {
        'type': 'local',
        'base_path': '/path/to/root'
    }

    valid_s3_configuration = {
        'type': 's3',
        'bucket_name': 'testbucket',
        'access_key_id': 'testaccesskeyid',
        'secret_access_key': 'testsecretaccesskey'
    }

    valid_configuration = {
        'source': valid_local_configuration,
        'destination': valid_s3_configuration
    }

    def test_can_get_local_storage_device_as_source(self):

        with patch(
                'configuration.Configuration.get',
                return_value=self.valid_configuration
        ):
            storage_device = SnapshotConfigurationReader.get_source()
            self.assertIsInstance(storage_device, LocalStorageDevice)
            self.assertEqual(
                self.valid_local_configuration['base_path'],
                storage_device.base_path
            )

    def test_can_get_local_storage_device_as_destination(self):

        configuration = {
            'source': self.valid_s3_configuration,
            'destination': self.valid_local_configuration
        }

        with patch(
                'configuration.Configuration.get',
                return_value=configuration
        ):
            storage_device = SnapshotConfigurationReader.get_destination()
            self.assertIsInstance(storage_device, LocalStorageDevice)
            self.assertEqual(
                self.valid_local_configuration['base_path'],
                storage_device.base_path
            )

    def test_can_get_s3_storage_device_as_source(self):

        configuration = {
            'source': self.valid_s3_configuration,
            'destination': self.valid_local_configuration
        }

        with patch(
                'configuration.Configuration.get',
                return_value=configuration
        ),\
                patch(
                    'storage_devices.s3.S3StorageDevice.__init__',
                    return_value=None
                ) as s3_initialiser:
            SnapshotConfigurationReader.get_source()
            s3_initialiser.assert_called_with(
                bucket_name=self.valid_s3_configuration['bucket_name'],
                access_key_id=self.valid_s3_configuration['access_key_id'],
                secret_access_key=self.valid_s3_configuration[
                    'secret_access_key'
                ],
            )

    def test_can_get_s3_storage_device_as_destination(self):

        with patch(
                'configuration.Configuration.get',
                return_value=self.valid_configuration
        ),\
                patch(
                    'storage_devices.s3.S3StorageDevice.__init__',
                    return_value=None
                ) as s3_initialiser:
            SnapshotConfigurationReader.get_destination()
            s3_initialiser.assert_called_with(
                bucket_name=self.valid_s3_configuration['bucket_name'],
                access_key_id=self.valid_s3_configuration['access_key_id'],
                secret_access_key=self.valid_s3_configuration[
                    'secret_access_key'
                ],
            )

    def test_raises_invalid_config_when_local_config_invalid(self):

        for key in self.valid_local_configuration.keys():
            local_configuration = self.valid_local_configuration.copy()
            del local_configuration[key]
            configuration = {
                'source': local_configuration,
                'destination': local_configuration
            }

            with patch(
                    'configuration.Configuration.get',
                    return_value=configuration
            ):
                with self.assertRaises(InvalidConfigurationError):
                    SnapshotConfigurationReader.get_source()
                with self.assertRaises(InvalidConfigurationError):
                    SnapshotConfigurationReader.get_destination()

    def test_raises_invalid_config_when_s3_config_invalid(self):

        for key in self.valid_s3_configuration.keys():
            s3_configuration = self.valid_s3_configuration.copy()
            del s3_configuration[key]
            configuration = {
                'source': s3_configuration,
                'destination': s3_configuration
            }

            with patch(
                    'configuration.Configuration.get',
                    return_value=configuration
            ):
                with self.assertRaises(InvalidConfigurationError):
                    SnapshotConfigurationReader.get_source()
                with self.assertRaises(InvalidConfigurationError):
                    SnapshotConfigurationReader.get_destination()

    def test_raises_invalid_config_when_type_is_unknown(self):

        for key in self.valid_s3_configuration.keys():
            configuration = self.valid_s3_configuration.copy()
            configuration['type'] = 'unknown'
            configuration = {
                'source': configuration,
                'destination': configuration
            }

            with patch(
                    'configuration.Configuration.get',
                    return_value=configuration
            ):
                with self.assertRaises(InvalidConfigurationError):
                    SnapshotConfigurationReader.get_source()
                with self.assertRaises(InvalidConfigurationError):
                    SnapshotConfigurationReader.get_destination()
