import time
from nosql import NoSqlDatabase
import matplotlib.pyplot as plt


class PerformanceCases(object):
    def __init__(self, name: str, number_of_cases: int, ylabel: str):
        self.number_of_cases = number_of_cases
        self.name = name
        self.ylabel = ylabel
        self._result = []
        self._max_value = 0
        self.fix, self._axd = plt.subplots()

    def test(self):
        pass

    def before_tests(self):
        pass

    def after_tests(self):
        pass

    def run(self):
        print("""Running {} test...""".format(self.name))
        self._before_tests()
        self.before_tests()
        for i in range(0, self.number_of_cases):
            self.before_test()
            self.test()
            self.after_test()
        self._after_tests()
        self.after_tests()

    def add_test_record(self, case):
        if case > self._max_value:
            self._max_value = case + case / 10
        self._result.append(case)

    def _before_tests(self):
        self._axd.set(xlabel='Case', ylabel=self.ylabel,
                      title=self.name)

    def _after_tests(self):
        self._axd.plot(
            range(1, self.number_of_cases + 1), self._result, 'ro', markersize=2
        )
        plt.savefig(self.name)

    def after_test(self):
        pass

    def before_test(self):
        pass


class CopyFromOneToAnotherDatabaseTest(PerformanceCases):
    def __init__(self, *args, **kwargs):
        PerformanceCases.__init__(self, number_of_cases=10, name="Operations per second per test case",
                                  ylabel="Operations per second")
        self.start = None
        self.mongodb2: NoSqlDatabase = None
        self.mongodb1: NoSqlDatabase = None

    def before_tests(self):
        self.mongodb2 = NoSqlDatabase(host='mongodb2', port=27017)
        self.mongodb1 = NoSqlDatabase(host='mongodb1', port=27017)

        self.mongodb1.drop()
        self.mongodb2.drop()
        self.mongodb1.save_random_record(100)

        print("""DB records:
mongodb1: {}
mongodb2: {}
        """.format(self.mongodb1.count(), self.mongodb2.count()))

    def before_test(self):
        self.mongodb1.reset_counter()
        self.mongodb2.reset_counter()
        self.mongodb2.drop()
        self.start = time.time()

    def test(self):
        while self.mongodb1.count() != self.mongodb2.count():
            record = self.mongodb1.get_random_record()
            credit_card_number = record['credit_card_number']

            while not self.mongodb2.credit_card_number_exist(credit_card_number):
                self.mongodb2.save_record(record)

    def after_test(self):
        end = time.time()
        self.add_test_record(
            (self.mongodb1.operation_counter + self.mongodb2.operation_counter) / (end - self.start)
        )


if __name__ == '__main__':
    print("Waiting for databases")
    time.sleep(10)
    CopyFromOneToAnotherDatabaseTest().run()
    plt.show()
