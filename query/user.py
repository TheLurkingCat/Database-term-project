from hashlib import pbkdf2_hmac
from os import urandom
from typing import Dict, List, Union

from sqlalchemy import (Boolean, Column, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine(
    'sqlite:///userinfo.db?check_same_thread=False')

metadata = MetaData(engine)
client = engine.connect()

user_table, history_meta_table, history_table = None, None, None


def create():
    global user_table, history_meta_table, history_table
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
        Column('use_month', Boolean, nullable=False),
        Column('avg', Boolean, nullable=False),
        Column('min', Boolean, nullable=False),
        Column('max', Boolean, nullable=False)
    )
    history_table = Table(
        'history', metadata,
        Column('username', String(100), nullable=False, primary_key=True),
        Column('search_type', String(16), nullable=False),
        Column('keyword', String(128), nullable=True)
    )
    metadata.create_all()


def load():
    global user_table, history_meta_table, history_table
    user_table = Table('user', metadata, autoload=True)
    history_meta_table = Table('history_meta', metadata, autoload=True)
    history_table = Table('history', metadata, autoload=True)


def register(username: str, password: str):
    error = None
    if len(username) > 100:
        error = True
    try:
        find_user(username, user_table)
    except StopIteration:
        error = False
    else:
        error = True
    finally:
        salt = urandom(64)
        key = pbkdf2_hmac('sha256', password.encode('UTF-8'), salt, 100000)

        new_user = user_table.insert(None).values(
            username=username, key=key, salt=salt)

        if error:
            raise KeyError("Username already exists.")
        client.execute(new_user)


def drop():
    metadata.drop_all()


def find_user(username: str, table: Table):
    query_user = table.select().where(table.c.username == username)
    result = next(client.execute(query_user))
    return result[1:]


def login(username: str, password: str):
    error = False
    try:
        key, salt = find_user(username, user_table)
    except StopIteration:
        error = True
    else:
        key_test = pbkdf2_hmac(
            'sha256', password.encode('UTF-8'), salt, 100000)

        if key_test == key:
            error = False
        else:
            error = True
    finally:
        if error:
            raise KeyError("Username or password is wrong.")
        print("WOW, you are now in.")


def log(username: str, meta: Dict[str, Union[str, int, bool]], compare_info: Dict[str, str]):
    query = history_meta_table.insert(None).values(**meta)
    try:
        client.execute(query)
    except SQLAlchemyError:
        update = history_meta_table.update(None).where(history_meta_table.c.username == username).values(
            **meta)
        client.execute(update)

    query = history_table.insert(None).values(**compare_info)
    try:
        client.execute(query)
    except SQLAlchemyError:
        update = history_table.update(None).where(history_table.c.username == username).values(
            **compare_info)
        client.execute(update)


def retrieve(username: str):
    query = history_table.select().where(history_table.c.username == username)
    history = client.execute(query)
    query = history_meta_table.select().where(
        history_meta_table.c.username == username)
    metadata = client.execute(query)
    return list(metadata) + list(history)


if __name__ == '__main__':
    create()
    # Test register
    register("meow", "Cats are cute.")

    # Test duplicate name
    try:
        register("meow", "Cats are cute.")
    except KeyError as err:
        print(str(err)[1:-1])

    # Test wrong username
    try:
        login("meowmeow", "Cats are cute.")
    except KeyError as err:
        print(str(err)[1:-1])

    # Test wrong password
    try:
        login("meow", "Cats are ugly.")
    except KeyError as err:
        print(str(err)[1:-1])

    # Test correct login
    login("meow", "Cats are cute.")

    # Clean up
    drop()
