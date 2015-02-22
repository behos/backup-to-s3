from database.models import FileReference
from snapshot.file_transporter import FileTransporter


class SnapshotRestorer(FileTransporter):

    def restore_snapshot(self, snapshot):

        for file_reference in snapshot.file_references:

            if not self._file_already_in_destination(file_reference):
                self._prepare_for_restore(file_reference)
                self._restore_file(file_reference)

    def _file_already_in_destination(self, file_reference):
        checksum = file_reference.checksum
        path = file_reference.path

        return (
            self.destination_storage_device.exists(path) and
            self.destination_storage_device.checksum(path) == checksum
        )

    def _prepare_for_restore(self, file_reference):
        path = file_reference.path
        if self.destination_storage_device.exists(path):
            self.destination_storage_device.delete(path)

    def _restore_file(self, file_reference):
        self.transfer_file(file_reference.backup_path, file_reference.path)

    def _add_file_reference_to_database(self, path, checksum, backup_path):
        file_reference = FileReference(
            path=path,
            checksum=checksum,
            backup_path=backup_path
        )
        self._get_session().add(file_reference)
        return file_reference
