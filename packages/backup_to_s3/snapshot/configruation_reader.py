from configuration import Configuration
from snapshot.exceptions import InvalidConfigurationError
from storage_devices.local import LocalStorageDevice
from storage_devices.s3 import S3StorageDevice


class SnapshotConfigurationReader(object):

    @classmethod
    def get_source(cls):
        source_configuration = Configuration.get()['source']
        return cls._get_storage_device_from_configuration(source_configuration)

    @classmethod
    def _get_storage_device_from_configuration(cls, configuration):
        type = cls._require(configuration, 'type')
        return cls._initialise_type(type, configuration)

    @classmethod
    def _require(cls, configuration, key):
        if key not in configuration:
            raise InvalidConfigurationError(
                '%s is required in snapshot configuration'
            )
        else:
            return configuration[key]

    @classmethod
    def _initialise_type(cls, type, configuration):
        if type not in _type_initialisers:
            raise InvalidConfigurationError(
                '%s is not a known type. Please use one of %s'
                % (type, _type_initialisers.keys())
            )
        return _type_initialisers[type](configuration)

    @classmethod
    def _initialise_local(cls, configuration):
        base_path = cls._require(configuration, 'base_path')
        return LocalStorageDevice(base_path=base_path)

    @classmethod
    def _initialise_s3(cls, configuration):
        bucket_name = cls._require(configuration, 'bucket_name')
        access_key_id = cls._require(configuration, 'access_key_id')
        secret_access_key = cls._require(configuration, 'secret_access_key')

        return S3StorageDevice(
            bucket_name=bucket_name,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key
        )

    @classmethod
    def get_destination(cls):
        source_configuration = Configuration.get()['destination']
        return cls._get_storage_device_from_configuration(source_configuration)


_type_initialisers = {
    'local': SnapshotConfigurationReader._initialise_local,
    's3': SnapshotConfigurationReader._initialise_s3,
}

__all__ = (
    SnapshotConfigurationReader,
)
