from hqlib.sql import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
import json
from datetime import datetime
from hqlib.sql.customtypes.textpickle import TextPickleType


class Worker(Base):

    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    target = Column(String)
    framework = Column(String)
    datacenter = Column(String)
    tags = Column(TextPickleType(pickler=json))
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime(timezone=True))
