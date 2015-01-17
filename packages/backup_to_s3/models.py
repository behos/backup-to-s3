from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, String, Integer

Base = declarative_base()


class BackedUpFile(Base):

    __tablename__ = "backed_up_file"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    path = Column(String, index=True, unique=True, nullable=False)
    last_backed_up_on = Column(DateTime, nullable=False)
    last_backed_up_hash = Column(String, nullable=False)
