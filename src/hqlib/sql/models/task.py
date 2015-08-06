from hqlib.sql import Base
from sqlalchemy import Column, Integer, String, ForeignKey, PickleType, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.orderinglist import ordering_list
from hqlib.sql.customtypes.enumtype import DBEnum
from hqlib.sql.customtypes.textpickle import TextPickleType
import json


class TaskStatus(DBEnum):
    PENDING = 'PENDING'
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    LOST = 'LOST'
    KILLED = 'KILLED'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'


class Task(Base):

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(TaskStatus.as_type('ck_task_status'), default=TaskStatus.PENDING, nullable=False)
    error_message = Column(String)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False)
    stopped_at = Column(DateTime(timezone=True))
    job_target_id = Column(Integer, ForeignKey('job_targets.id'))
    job_target = relationship('JobTarget', uselist=False)
    actions = relationship('Action', order_by='Action.order', collection_class=ordering_list('order'))


class Action(Base):

    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    processor = Column(String, nullable=False)
    arguments = Column(TextPickleType(pickler=json))
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    task = relationship('Task', uselist=False)
