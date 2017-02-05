from sqlalchemy import MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from config import DEST_DATABASE_URI
from db_functions import make_session, quick_mapper
import re


PHONE_LENGTH = 10


def get_normalized_phone(phone):
    return re.sub(r'\D', '', phone)[-PHONE_LENGTH:]


def run_normalize(session, engine):
    meta = MetaData(bind=engine)
    table = Table('orders', meta, autoload=True)
    table_class = quick_mapper(table)
    for record in session.query(table_class).all():
        record.normalized_phone = get_normalized_phone(record.contact_phone)


if __name__ == '__main__':
    session, engine = make_session(DEST_DATABASE_URI)
    try:
        run_normalize(session, engine)
        session.commit()
        print('Normalization is completed successfully!')
    except SQLAlchemyError:
        session.rollback()
        print('DB connection error!')
        raise
