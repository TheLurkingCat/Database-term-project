from sqlalchemy import (Boolean, Column, Integer, MetaData, String, Table,
                        create_engine)


def create(metadata: MetaData):
    user_table = Table(
        'user', metadata,
        Column('username', String(100), nullable=False, primary_key=True),
        Column('key', String(32), nullable=False),
        Column('salt', String(64), nullable=False)
    )
    history_meta_table = Table(
        'history_meta', metadata,
        Column('username', String(100), nullable=False, primary_key=True),
        Column('year_start', Integer, nullable=False),
        Column('month_start', Integer, nullable=False),
        Column('year_end', Integer, nullable=False),
        Column('month_end', Integer, nullable=False),
        Column('use_bar', Boolean, nullable=False),
        Column('use_month', Boolean, nullable=False)
    )
    history_table = Table(
        'history', metadata,
        Column('username', String(100), nullable=False, primary_key=True),
        Column('search_type', String(16), nullable=False),
        Column('keyword', String(128), nullable=False)
    )
    metadata.create_all()
    return user_table, history_meta_table, history_table


def drop(metadata: MetaData):
    metadata.drop_all()


def load(metadata: MetaData):
    user_table = Table('user', metadata, autoload=True)
    history_meta_table = Table('history_meta', metadata, autoload=True)
    history_table = Table('history', metadata, autoload=True)
    return user_table, history_meta_table, history_table


if __name__ == '__main__':
    engine = create_engine(
        'sqlite:///userinfo.db?check_same_thread=False')
    drop(MetaData(engine))
