import hashlib
import os
from shutil import copyfile
from storage_devices.base import StorageDevice
from storage_devices.exceptions import StorageDeviceError


class LocalStorageDevice(StorageDevice):

    def __init__(self, base_path):
        self.base_path = os.path.realpath(base_path)

    def _get_absolute_path(self, path):
        return os.path.join(self.base_path, path)

    def put(self, source_path, destination_path):
        if self.exists(destination_path):
            raise FileExistsError(
                'File %s already exists' % destination_path
            )
        elif self._path_belongs_to_storage_device(source_path):
            raise StorageDeviceError(
                'Source cannot be within storage device path'
            )
        else:
            absolute_path = self._get_absolute_path(destination_path)
            absolute_dirname = os.path.dirname(absolute_path)
            if not os.path.exists(absolute_dirname):
                os.makedirs(absolute_dirname)
            elif not os.path.isdir(absolute_dirname):
                raise NotADirectoryError(
                    '%s is not a directory' % absolute_dirname
                )

            copyfile(
                source_path,
                absolute_path
            )

    def _path_belongs_to_storage_device(self, path):
        return os.path.realpath(path).startswith(self.base_path)

    def get(self, path, destination_path):
        if not self.exists(path):
            raise FileNotFoundError('Could not find file %s' % path)
        elif self._path_belongs_to_storage_device(destination_path):
            raise StorageDeviceError(
                'Destination cannot be within storage device path'
            )
        else:
            copyfile(self._get_absolute_path(path), destination_path)

    def exists(self, path):
        return os.path.exists(self._get_absolute_path(path))

    def size(self, path):
        return os.path.getsize(self._get_absolute_path(path))

    def list(self):
        file_list = []
        for root, dirs, files in os.walk(self.base_path):
            for basename in files:
                filename = os.path.join(root, basename)
                filename = self._strip_base_path(filename)
                file_list.append(filename)

        return file_list

    def _strip_base_path(self, filename):
        filename = filename.replace("%s%s" % (self.base_path, os.path.sep), '')
        return filename

    def delete(self, path):
        if not self.exists(path):
            raise FileNotFoundError('Could not find file %s' % path)
        os.remove(self._get_absolute_path(path))

    def checksum(self, path):
        if not self.exists(path):
            raise FileNotFoundError('Could not find file %s' % path)

        return self._calculate_checksum(self._get_absolute_path(path))

    def _calculate_checksum(self, path):
        md5_hasher = hashlib.md5()
        block_size = 65536

        with open(path, 'rb') as file:
            buffer = file.read(block_size)
            while len(buffer) > 0:
                md5_hasher.update(buffer)
                buffer = file.read(65536)

        return md5_hasher.hexdigest()
