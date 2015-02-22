import sys
import os
import argparse

sys.path.append(os.path.dirname(__file__))

from snapshot.controller import SnapshotController
from snapshot.selector import SnapshotSelector
from database.configuration_reader import DatabaseConfigurationReader
from database.controller import DatabaseController
from snapshot.exceptions import InvalidConfigurationError

parser = argparse.ArgumentParser()
parser.add_argument(
    '-r', '--restore',
    help='Restore a taken snapshot',
    action='store_true'
)

args = parser.parse_args()

try:
    database_path = DatabaseConfigurationReader.get_path()
    DatabaseController.setup(database_path)

    if args.restore:
        try:
            snapshot = SnapshotSelector().select_snapshot()
            SnapshotController.restore_snapshot(snapshot)
        except KeyboardInterrupt:
            print('\nCancelling restore')
    else:
        SnapshotController.take_snapshot()

except InvalidConfigurationError as e:
    sys.stderr.write('Invalid configuration: %s' % e)
    sys.exit(1)
