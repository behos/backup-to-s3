from datetime import datetime
from inflection import underscore
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative.api import declared_attr, declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import Column, UniqueConstraint, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, DateTime


class Base(object):

    @declared_attr
    def __tablename__(cls):
        return underscore(cls.__name__)

    __table_args__ = ({'sqlite_autoincrement': True},)

Base = declarative_base(cls=Base)


class IdMixin(object):
    id = Column(Integer, primary_key=True)


class FileReference(IdMixin, Base):

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint('path', 'hash'),) + Base.__table_args__

    path = Column(String, index=True, nullable=False)
    backup_path = Column(String, unique=True, nullable=False)
    hash = Column(String, nullable=False)


class Snapshot(IdMixin, Base):
    time = Column(DateTime, nullable=False, default=datetime.utcnow())
    file_references = association_proxy(
        'file_references_in_snapshot',
        'file_reference'
    )


class FileReferenceInSnapshot(Base):
    file_reference_id = Column(
        Integer,
        ForeignKey('%s.id' % FileReference.__tablename__),
        primary_key=True
    )

    file_reference = relationship(
        FileReference,
        backref=backref("file_references_in_snapshot", cascade="all")
    )

    snapshot_id = Column(
        Integer,
        ForeignKey('%s.id' % Snapshot.__tablename__),
        primary_key=True
    )

    snapshot = relationship(
        Snapshot,
        backref=backref('file_references_in_snapshot', cascade="all")
    )

    def __init__(self, file_reference=None, snapshot=None):
        self.file_reference = file_reference
        self.snapshot = snapshot
