from inflection import underscore
from sqlalchemy.ext.declarative.api import declared_attr, declarative_base
from sqlalchemy.sql.schema import Column, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer


class Base(object):

    @declared_attr
    def __tablename__(cls):
        return underscore(cls.__name__)

    __table_args__ = ({'sqlite_autoincrement': True},)

    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)


class FileReference(Base):

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint('path', 'hash'),) + Base.__table_args__

    path = Column(String, index=True, nullable=False)
    backup_path = Column(String, unique=True, nullable=False)
    hash = Column(String, nullable=False)
