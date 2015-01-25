from configuration import Configuration
from snapshot.exceptions import InvalidConfigurationError


class DatabaseConfigurationReader(object):

    @classmethod
    def get_path(cls):
        configuration = Configuration.get()
        if 'database_path' not in configuration:
            raise InvalidConfigurationError(
                'Database path missing from configuration'
            )
        return configuration['database_path']
