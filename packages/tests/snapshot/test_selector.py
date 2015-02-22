from unittest.case import TestCase
from unittest.mock import patch
from tests.util import DatabaseTestMixin
from database.models import Snapshot
from snapshot.exceptions import RestoreSnapshotError
from snapshot.selector import SnapshotSelector


class TestSnapshotSelector(
    DatabaseTestMixin,
    TestCase
):

    def test_throws_error_if_no_snapshots_exist(self):
        with patch('snapshot.selector.SnapshotSelector._get_user_choice'):
            with self.assertRaises(RestoreSnapshotError):
                SnapshotSelector().select_snapshot()

    def test_selects_snapshot_by_id(self):
        snapshot = self._create_snapshot()
        with patch(
            'snapshot.selector.SnapshotSelector._get_user_input',
            return_value=snapshot.id
        ):
            selected_snapshot = SnapshotSelector().select_snapshot()

        self.assertEqual(snapshot.id, selected_snapshot.id)

    def test_can_recover_from_non_int_input(self):
        snapshot = self._create_snapshot()
        with patch(
            'snapshot.selector.SnapshotSelector._get_user_input',
            wraps=self._generate_user_input('a', 'b', snapshot.id)
        ):
            selected_snapshot = SnapshotSelector().select_snapshot()

        self.assertEqual(snapshot.id, selected_snapshot.id)

    def test_can_only_accept_an_existing_snapshot_id(self):
        snapshot = self._create_snapshot()
        with patch(
            'snapshot.selector.SnapshotSelector._get_user_input',
            wraps=self._generate_user_input(snapshot.id + 1, snapshot.id)
        ):
            selected_snapshot = SnapshotSelector().select_snapshot()

        self.assertEqual(snapshot.id, selected_snapshot.id)

    def _create_snapshot(self):
        snapshot = Snapshot()
        self.db_session.add(snapshot)
        self.db_session.flush()
        return snapshot

    def _generate_user_input(self, *list_of_values):
        def get_input():
            for value in list_of_values:
                yield value

        value_generator = get_input()

        def value_getter():
            return value_generator.__next__()

        return value_getter
