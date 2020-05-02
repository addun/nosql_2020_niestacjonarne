from nosql import NoSqlDatabase

if __name__ == '__main__':
    NoSqlDatabase(port=25001).save_random_record(100)
