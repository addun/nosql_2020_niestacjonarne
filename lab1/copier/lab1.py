import datetime
import json
import time

from mysql.connector import (connection)
from pymongo import MongoClient


def get_entity_names(entity):
    return [x for x in dir(entity) if isinstance(getattr(entity, x), EntityColumn)]


class Entity(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)


class EntityColumn:
    pass


class TestEntity(Entity):
    column1 = EntityColumn()
    column3 = EntityColumn()


class SqlDatabase:
    def __init__(self):
        self._database = connection.MySQLConnection(
            host="mariadb",
            user="root",
            passwd="password",
            database="COPIER",
        )

    def select_all_from_test(self):
        return self._select_all_from("test", TestEntity)

    def _select_all_from(self, table, entity):
        c = self._database.cursor()
        attrs = [x for x in dir(entity) if isinstance(getattr(entity, x), EntityColumn)]
        a = ", ".join(attrs)
        c.execute("SELECT {} FROM {};".format(a, table))
        records = []
        for items in c:
            e = entity()
            for i in range(0, len(items)):
                e[attrs[i]] = items[i]
            records.append(e)
        c.close()
        return records


class NoSqlDatabase:
    def __init__(self):
        self._client = MongoClient('mongodb://mongodb:27017/',
                                   username='root',
                                   password='password')
        self._database = self._client.COPIER

    def clear_test(self):
        self._database.test.drop()

    def save_in_test(self, records):
        data = json.loads(json.dumps(records))
        [self._database.test.insert_one(x) for x in data]


if __name__ == '__main__':
    sqlDatabase = SqlDatabase()
    print("Getting records from SQL database")
    start = time.time()
    rows = sqlDatabase.select_all_from_test()
    end = time.time()
    print("{} items have been downloaded in {}s".format(len(rows), end - start))

    noSqlDatabase = NoSqlDatabase()
    noSqlDatabase.clear_test()
    print("Adding records to NoSQL database")
    start = time.time()
    noSqlDatabase.save_in_test(rows)
    end = time.time()
    print("Items have been added in {}s".format(end - start))
