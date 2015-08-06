from hqlib.sql import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from hqlib.sql.customtypes.enumtype import DBEnum
from sqlalchemy.ext.orderinglist import ordering_list
from hqlib.sql.customtypes.textpickle import TextPickleType
import json


class JobStatus(DBEnum):

    PENDING = 'PENDING'
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'
    COMPLETED = 'COMPLETED'


class Job(Base):

    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    current_task_index = Column(Integer, default=0, nullable=False)
    status = Column(JobStatus.as_type('ck_job_status'), default=JobStatus.PENDING, nullable=False)
    datacenter = Column(String, nullable=False)
    tags = Column(TextPickleType(pickler=json))
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False)
    stopped_at = Column(DateTime(timezone=True))
    user_assignment_id = Column(Integer, ForeignKey('user_assignments.id'), nullable=False)
    assignment = relationship("UserAssignment", uselist=False)
    targets = relationship('JobTarget', backref='jobs')


class JobTarget(Base):

    __tablename__ = 'job_targets'

    id = Column(Integer, primary_key=True)
    tags = Column(TextPickleType(pickler=json))
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    job = relationship('Job', uselist=False)
    worker = relationship('Worker', uselist=False)
    tasks = relationship('Task', order_by='Task.order', collection_class=ordering_list('order'))
