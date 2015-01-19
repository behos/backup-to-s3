import yaml
import os


class Configuration(object):

    @classmethod
    def get(cls):
        if not hasattr(cls, '_configuration'):
            with open(cls._configuration_path(), 'r') as config_file:
                cls._configuration = yaml.load(config_file)
        return cls._configuration

    @classmethod
    def _configuration_path(cls):
        home = os.path.expanduser('~')
        return os.path.join(home, '.backup-to-s3', 'config.yml')
