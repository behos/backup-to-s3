from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, String

Base = declarative_base()


class BackedUpFile(Base):

    __tablename__ = "backed_up_file"

    id = Column(BigInteger, primary_key=True)
    path = Column(String, index=True, unique=True)
    last_backed_up_on = Column(DateTime)
    last_backed_up_hash = Column(String)
