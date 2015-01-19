import math
from boto.s3.key import Key
from filechunkio.filechunkio import FileChunkIO
import os
from boto.s3.connection import S3Connection


class S3StorageDevice(object):

    chunk_size = 52428800

    def __init__(self, bucket_name, access_key_id, secret_access_key):
        self.connection = S3Connection(access_key_id, secret_access_key)
        self.bucket = self.connection.get_bucket(bucket_name)

    def put(self, source_path, destination_path):
        if self.exists(destination_path):
            raise FileExistsError("Key %s already exists" % destination_path)
        source_size = os.stat(source_path).st_size
        if source_size > self.chunk_size:
            self._upload_in_chunks(source_path, destination_path)

        else:
            self._upload(source_path, destination_path)

    def _upload_in_chunks(self, source_path, destination_path):
        source_size = os.stat(source_path).st_size

        multipart_upload = self.bucket.initiate_multipart_upload(
            destination_path
        )

        chunk_count = int(math.ceil(source_size / self.chunk_size))

        for i in range(chunk_count + 1):
            offset = self.chunk_size * i
            bytes = min(self.chunk_size, source_size - offset)
            with FileChunkIO(
                    source_path,
                    'r',
                    offset=offset,
                    bytes=bytes
            ) as fp:
                multipart_upload.upload_part_from_file(fp, part_num=i + 1)

        multipart_upload.complete_upload()

    def _upload(self, source_path, destination_path):
        key = Key(self.bucket)
        key.key = destination_path
        key.set_contents_from_filename(source_path)

    def get(self, path, to_path):
        if self.exists(path):
            key = self.bucket.get_key(path)
            key.get_contents_to_filename(to_path)
        else:
            raise FileNotFoundError("Could not find key %s" % path)

    def exists(self, path):
        key = Key(self.bucket, path)
        return key.exists()

    def size(self, path):
        key = self.bucket.get_key(path)
        return key.size

    def list(self):
        return [key.key for key in self.bucket.get_all_keys()]

    def delete(self, path):
        if self.exists(path):
            key = self.bucket.get_key(path)
            key.delete()
        else:
            raise FileNotFoundError("Could not find key %s" % path)
