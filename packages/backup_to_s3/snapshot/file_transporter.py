from tempfile import NamedTemporaryFile
import os


class FileTransporter(object):

    def __init__(
            self,
            source_storage_device,
            destination_storage_device
    ):
        self.source_storage_device = source_storage_device
        self.destination_storage_device = destination_storage_device

    def transfer_file(self, source_path, destination_path):
        temp_file = NamedTemporaryFile(delete=False)
        temp_path = os.path.realpath(temp_file.name)
        self.source_storage_device.get(source_path, temp_path)
        self.destination_storage_device.put(temp_path, destination_path)
        os.remove(temp_path)
