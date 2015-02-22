from snapshot.configuration_reader import SnapshotConfigurationReader
from snapshot.restorer import SnapshotRestorer
from snapshot.taker import SnapshotTaker


class SnapshotController(object):

    @staticmethod
    def take_snapshot():
        storage, backup_storage = \
            SnapshotController._get_storage_devices_from_configuration()

        snapshot_taker = SnapshotTaker(
            source_storage_device=storage,
            destination_storage_device=backup_storage
        )

        snapshot_taker.take_snapshot()

    @staticmethod
    def restore_snapshot(snapshot):
        storage, backup_storage = \
            SnapshotController._get_storage_devices_from_configuration()

        snapshot_restorer = SnapshotRestorer(
            source_storage_device=backup_storage,
            destination_storage_device=storage
        )
        snapshot_restorer.restore_snapshot(
            snapshot=snapshot
        )

    @staticmethod
    def _get_storage_devices_from_configuration():
        storage = SnapshotConfigurationReader.get_source()
        backup_storage = SnapshotConfigurationReader.get_destination()
        return storage, backup_storage
