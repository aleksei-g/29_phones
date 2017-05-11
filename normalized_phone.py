from sqlalchemy import MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from config import DEST_DATABASE_URI
from db_functions import make_session, quick_mapper
import re
from time import sleep


PHONE_LENGTH = 10
DELAY = 30


def run_query(f):
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
    return wrapper


def get_normalized_phone(phone):
    return re.sub(r'\D', '', phone)[-PHONE_LENGTH:]


@run_query
def run_normalize(session, engine):
    meta = MetaData(bind=engine)
    table = Table('orders', meta, autoload=True)
    table_class = quick_mapper(table)
    for record in session.query(table_class).filter(
            table_class.normalized_phone.is_(None)):
        record.normalized_phone = get_normalized_phone(record.contact_phone)


if __name__ == '__main__':
    session, engine = make_session(DEST_DATABASE_URI)
    while True:
        try:
            run_normalize(session, engine)
            sleep(DELAY)
        except KeyboardInterrupt:
            print('exit')
            break
