from sqlalchemy import Column, MetaData, String, Table


def create(metadata: MetaData):
    user_table = Table('user', metadata, Column('username', String(
        100), primary_key=True, nullable=False), Column('key', String(32), nullable=False), Column('salt', String(64), nullable=False))
    history_table = Table('history', metadata)
    metadata.create_all()
    return user_table, history_table


def drop(metadata: MetaData):
    metadata.drop_all()


def load(metadata: MetaData):
    user_table = Table('user', metadata, autoload=True)
    history_table = Table('history', metadata, autoload=True)
    return user_table, history_table
