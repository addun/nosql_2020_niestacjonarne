from nosql import NoSqlDatabase

if __name__ == '__main__':
    NoSqlDatabase(host='mongodb1',port=27017).save_random_record(100)
