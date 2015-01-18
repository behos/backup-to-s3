from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker


class DatabaseController(object):

    def __init__(self, database_path=''):
        self._connect(database_path)
        self._create_all()
        self._create_session_class()

    def _connect(self, database_path):
        if database_path:
            database_path = '/%s' % database_path

        self.db = create_engine('sqlite://' + database_path)

    def _create_all(self):
        from models import Base
        Base.metadata.bind = self.db
        Base.metadata.create_all()

    def _create_session_class(self):
        self.Session = sessionmaker(bind=self.db)

    def get_session(self):
        return self.Session()
