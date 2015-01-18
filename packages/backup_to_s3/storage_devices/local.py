
class LocalStorageDevice(object):

    def __init__(self, base_path):
        self.base_path = base_path

    def put_file(self, file, path):
        raise NotImplementedError()

    def get_file(self, path):
        raise NotImplementedError()

    def get_file_list(self):
        raise NotImplementedError()
