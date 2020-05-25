import uuid

TABLE_NAME = 'test'
COLUMN_NAME_1 = 'column1'
COLUMN_NAME_2 = 'column3'
DB_NAME = 'COPIER'


def create_db() -> str:
    return "CREATE DATABASE IF NOT EXISTS {} ;".format(DB_NAME)


def use_db() -> str:
    return "USE {};".format(DB_NAME)


def drop_table() -> str:
    return "DROP TABLE IF EXISTS  {};".format(TABLE_NAME)


def create_random_row() -> str:
    return "INSERT INTO {} ({}, {}) VALUES ('{}', '{}');".format(TABLE_NAME, COLUMN_NAME_1, COLUMN_NAME_2,
                                                                  uuid.uuid4(), uuid.uuid4())


def create_table() -> str:
    return "CREATE TABLE {} ({} varchar(255), {} varchar(255)) ;".format(TABLE_NAME, COLUMN_NAME_1, COLUMN_NAME_2)


if __name__ == '__main__':
    with open("lab1.sql", "w+") as f:
        n = 5
        f.write(create_db() + "\n")
        f.write(use_db() + "\n")
        f.write(drop_table() + "\n")
        f.write(create_table() + "\n")
        [f.write(create_random_row() + "\n") for i in range(0, pow(10, n))]
