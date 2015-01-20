from models import Snapshot, Session
import os
from tempfile import NamedTemporaryFile


class SnapshotTaker(object):

    def __init__(
            self,
            source_storage_device,
            destination_storage_device
    ):
        self.source_storage_device = source_storage_device
        self.destination_storage_device = destination_storage_device

    def _transfer_file(self, source_path, destination_path):
        temp_file = NamedTemporaryFile(delete=False)
        temp_path = os.path.realpath(temp_file.name)
        self.source_storage_device.get(source_path, temp_path)
        self.destination_storage_device.put(temp_path, destination_path)
        os.remove(temp_path)

    def take_snapshot(self):
        db_session = Session()

        snapshot = Snapshot()
        db_session.add(snapshot)
        db_session.flush()

        for path in self.source_storage_device.list():
            self._transfer_file(path, path + ".1")

        db_session.commit()
