from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from sqlalchemy.pool import QueuePool

Base = declarative_base()


class SQLDB(object):

    def __init__(self, sql_config):
        self.driver = sql_config.driver
        self.host = sql_config.host
        self.port = sql_config.port
        self.database = sql_config.database
        self.username = sql_config.username
        self.password = sql_config.password
        self.pool_size = sql_config.pool_size
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
        self.engine = create_engine(URL(**database),
                                    poolclass=QueuePool,
                                    pool_size=self.pool_size)

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
