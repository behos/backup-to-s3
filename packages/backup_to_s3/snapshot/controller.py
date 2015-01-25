from snapshot.configuration_reader import SnapshotConfigurationReader
from snapshot.taker import SnapshotTaker


class SnapshotController(object):

    @staticmethod
    def take_snapshot():
        source = SnapshotConfigurationReader.get_source()
        destination = SnapshotConfigurationReader.get_destination()
        snapshot_taker = SnapshotTaker(
            source_storage_device=source,
            destination_storage_device=destination
        )

        snapshot_taker.take_snapshot()
