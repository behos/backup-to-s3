from models import Session, Base
from sqlalchemy.engine import create_engine


class DatabaseController(object):

    @classmethod
    def setup(cls, database_path=''):
        if database_path:
            database_path = '/%s' % database_path

        engine = create_engine('sqlite://' + database_path)

        Session.configure(bind=engine)
        Base.metadata.bind = engine
        Base.metadata.create_all()
