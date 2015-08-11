from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from sqlalchemy.pool import QueuePool

Base = declarative_base()


class SQLDB(object):

    def __init__(self, driver, host, port, database, username, password, pool_size):
        self.driver = driver
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.pool_size = pool_size
        self.engine = None

    def connect(self):
        database = {
            'drivername': self.driver,
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'database': self.database
        }
        self.engine = create_engine(URL(**database), poolclass=QueuePool, pool_size=self.pool_size)

    @contextmanager
    def session(self):

        session = scoped_session(sessionmaker())
        session.configure(bind=self.engine)
        session = session()

        session.execute('SELECT 1').scalar()

        try:
            yield session
        finally:
            scoped_session(sessionmaker()).remove()
