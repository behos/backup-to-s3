import datetime

from models import Snapshot, Session, FileReference
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

    def _get_session(self):
        if not hasattr(self, '_db_session'):
            self._db_session = Session()
        return self._db_session

    def _commit_session(self):
        self._get_session().commit()
        del self._db_session

    def take_snapshot(self):
        db_session = self._get_session()

        snapshot = Snapshot()
        db_session.add(snapshot)
        db_session.flush()

        for path in self.source_storage_device.list():
            checksum = self.source_storage_device.checksum(path)
            existing_file_query = db_session.query(FileReference).filter(
                FileReference.path == path,
                FileReference.checksum == checksum
            )

            if existing_file_query.count() == 1:
                file_reference = existing_file_query.first()
            else:
                backup_path = self._backup_file(path)
                file_reference = self._add_file_reference_to_database(
                    path,
                    checksum,
                    backup_path
                )
            snapshot.file_references.append(file_reference)

        self._commit_session()

    def _backup_file(self, path):
        backup_path = '%s_%s' % (path, datetime.datetime.now())
        self._transfer_file(path, backup_path)
        return backup_path

    def _add_file_reference_to_database(self, path, checksum, backup_path):
        file_reference = FileReference(
            path=path,
            checksum=checksum,
            backup_path=backup_path
        )
        self._get_session().add(file_reference)
        return file_reference
