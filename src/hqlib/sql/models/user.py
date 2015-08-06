from hqlib.sql import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=False)


class UserAssignment(Base):

    __tablename__ = 'user_assignments'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    token_id = Column(Integer, ForeignKey('tokens.id'))
    token = relationship('Token', uselist=False)
    permissions = relationship('Permission')
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False)


class Token(Base):

    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False)


class Permission(Base):

    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    permission = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    user_assignment_id = Column(Integer, ForeignKey('user_assignments.id'), nullable=False)
