from faker import Faker
from pymongo import MongoClient


def create_record():
    fake = Faker()

    return {
        'name': fake.name(),
        'address': fake.address(),
        'job': fake.job(),
        'born': fake.date(),
        'company': fake.company(),
        'credit_card_number': fake.credit_card_number(),
        'license_plate': fake.license_plate()
    }


class NoSqlDatabase:
    def __init__(self, host='0.0.0.0', port='27017', *args, **kwargs):
        self._client = MongoClient('mongodb://{}:{}/'.format(host, port),
                                   username='root',
                                   password='password')
        self._database = self._client.COPIER
        self._collection = self._database.performance_test
        self.operation_counter = 0

    def reset_counter(self):
        self.operation_counter = 0

    def increase_counter(self):
        self.operation_counter = self.operation_counter + 1

    def get_credit_card_number(self, credit_card_number):
        self.increase_counter()
        return self._collection.findOne({'credit_card_number': credit_card_number})

    def credit_card_number_exist(self, credit_card_number):
        self.increase_counter()
        return len(list(self._collection.find({'credit_card_number': credit_card_number}).limit(1))) == 1

    def save_record(self, record):
        self.increase_counter()
        self._collection.insert_one(record)

    def get_random_record(self):
        self.increase_counter()
        return list(self._collection.aggregate([{'$sample': {'size': 1}}]))[0]

    def count(self):
        return self._collection.count()

    def drop(self):
        return self._collection.drop()

    def save_random_record(self, how_many):
        [self.save_record(create_record()) for i in range(0, how_many)]
