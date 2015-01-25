from unittest.case import TestCase
from unittest.mock import patch
from snapshot.controller import SnapshotController


class TestSnapshotController(TestCase):

    def test_snapshot_controller_initialises_and_runs_snapshot_taker(self):

        mock_source = object()
        mock_destination = object()

        with patch('snapshot.configuration_reader.'
                   'SnapshotConfigurationReader.get_source',
                   return_value=mock_source), \
            patch('snapshot.configuration_reader.'
                  'SnapshotConfigurationReader.get_destination',
                  return_value=mock_destination), \
            patch('snapshot.taker.SnapshotTaker.__init__',
                  return_value=None) as snapshot_initialiser, \
            patch('snapshot.taker.'
                  'SnapshotTaker.take_snapshot') as mock_take_snapshot:
                SnapshotController.take_snapshot()

        snapshot_initialiser.assert_called_with(
            source_storage_device=mock_source,
            destination_storage_device=mock_destination
        )
        assert mock_take_snapshot.called
