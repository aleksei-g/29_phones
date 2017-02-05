from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def make_session(connection_string):
    engine = create_engine(connection_string, echo=False, convert_unicode=True)
    session = sessionmaker(bind=engine)
    return session(), engine


def quick_mapper(table):
    base = declarative_base()

    class GenericMapper(base):
        __table__ = table
    return GenericMapper
