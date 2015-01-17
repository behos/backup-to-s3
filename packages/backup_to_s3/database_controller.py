from sqlalchemy import create_engine
from models import Base


class DatabaseController(object):

    @staticmethod
    def initialise(self):
        Base.create_all()
