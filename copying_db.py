from sqlalchemy import MetaData, Table
from config import SOURCE_DATABASE_URI, DEST_DATABASE_URI, TABLES
from db_functions import make_session, quick_mapper


def pull_data(from_db, to_db, tables):
    source_session, source_engine = make_session(from_db)
    source_meta = MetaData(bind=source_engine)
    destination_source, destination_engine = make_session(to_db)
    for table_name in tables:
        print('Processing', table_name)
        print('Pulling schema from source server')
        table = Table(table_name, source_meta, autoload=True)
        print('Creating table on destination server')
        table.metadata.create_all(destination_engine)
        new_record = quick_mapper(table)
        columns = table.columns.keys()
        print('Transferring records')
        for record in source_session.query(table).all():
            data = dict(
                [(str(column), getattr(record, column)) for column in columns]
            )
            destination_source.merge(new_record(**data))
    print('Committing changes')
    destination_source.commit()


if __name__ == '__main__':
    pull_data(SOURCE_DATABASE_URI, DEST_DATABASE_URI, TABLES)
