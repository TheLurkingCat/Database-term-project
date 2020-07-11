from hashlib import pbkdf2_hmac
from os import urandom

from sqlalchemy import MetaData, Table, create_engine

import dbutils

engine = create_engine(
    'sqlite:///userinfo.db?check_same_thread=False')

metadata = MetaData(engine)
client = engine.connect()

user_table, history_table = dbutils.create(metadata)


def register(username: str, password: str):
    error = None
    if len(username) > 100:
        error = True
    try:
        query(username, user_table)
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


def query(username: str, table: Table):
    query_user = table.select().where(table.c.username == username)
    result = next(client.execute(query_user))
    return result[1:]


def login(username: str, password: str):
    error = False
    try:
        key, salt = query(username, user_table)
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


def log(last_params: dict):
    client.execute(history_table.insert(None), [last_params])


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
dbutils.drop(metadata)
