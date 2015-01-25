import sys
import os

sys.path.append(os.path.dirname(__file__))

from snapshot.controller import SnapshotController

SnapshotController.take_snapshot()
