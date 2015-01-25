import sys

import os

sys.path.append(os.path.dirname(__file__))

from snapshot.controller import SnapshotController
from database.configuration_reader import DatabaseConfigurationReader
from database.controller import DatabaseController
from snapshot.exceptions import InvalidConfigurationError

try:
    database_path = DatabaseConfigurationReader.get_path()
    DatabaseController.setup(database_path)
    SnapshotController.take_snapshot()
except InvalidConfigurationError as e:
    print("Invalid configuration: %s" % e)
