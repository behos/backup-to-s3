from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.sql.schema import Column, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer

Base = declarative_base()


class FileReference(Base):

    __tablename__ = "file_reference"
    __table_args__ = (
        UniqueConstraint('path', 'hash'),
        {
            'sqlite_autoincrement': True,
        }
    )

    id = Column(Integer, primary_key=True)
    path = Column(String, index=True, nullable=False)
    backup_path = Column(String, unique=True, nullable=False)
    hash = Column(String, nullable=False)
