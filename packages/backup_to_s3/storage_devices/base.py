class StorageDevice(object):

    def put_file(self, file, path):
        raise NotImplementedError()

    def get_file(self, path):
        raise NotImplementedError()

    def get_file_list(self):
        raise NotImplementedError()
