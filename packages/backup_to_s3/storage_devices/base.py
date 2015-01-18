class StorageDevice(object):

    def put(self, file, path):
        raise NotImplementedError()

    def get(self, path, to_path):
        raise NotImplementedError()

    def exists(self, path):
        raise NotImplementedError()

    def size(self, path):
        raise NotImplementedError()

    def list(self):
        raise NotImplementedError()

    def delete(self, path):
        raise NotImplementedError()
