import sys

import os

sys.path.append(os.path.dirname(__file__))

from snapshot.controller import SnapshotController
from database.configuration_reader import DatabaseConfigurationReader
from database.controller import DatabaseController

database_path = DatabaseConfigurationReader.get_path()
DatabaseController.setup(database_path)
SnapshotController.take_snapshot()
