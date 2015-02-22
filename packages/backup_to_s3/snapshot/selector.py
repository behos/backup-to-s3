from database.models import Session, Snapshot
from snapshot.exceptions import RestoreSnapshotError


class SnapshotSelector(object):

    def _get_session(self):
        if not hasattr(self, '_db_session'):
            self._db_session = Session()
        return self._db_session

    def select_snapshot(self):
        self._print_snapshot_list()
        return self._get_user_choice()

    def _print_snapshot_list(self):
        for line in self._get_snapshot_string_list():
            print(line)

    def _get_snapshot_string_list(self):
        snapshots = self._get_session()\
            .query(Snapshot).order_by(Snapshot.time.desc()).all()
        if not snapshots:
            raise RestoreSnapshotError("No snapshots to restore")
        return [self._get_snapshot_string(snapshot) for snapshot in snapshots]

    @staticmethod
    def _get_snapshot_string(snapshot):
        return '[%d] Taken at %s' % (
            snapshot.id,
            snapshot.time.strftime('%d %h %Y %H:%m')
        )

    def _get_user_choice(self):
        while True:
            try:
                choice = int(self._get_user_input())

                snapshot = self._get_chosen_snapshot(choice)
                if snapshot:
                    return snapshot
                else:
                    print('%s is not a valid choice' % choice)

            except ValueError:
                print('Please input an integer')

    def _get_chosen_snapshot(self, choice):
        return self._get_session().query(Snapshot).filter(Snapshot.id == choice).first()

    @staticmethod
    def _get_user_input():
        return input(
            'Please select snapshot to restore (Ctrl-C to cancel): '
        )
