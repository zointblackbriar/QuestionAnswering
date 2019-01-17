import unittest
import os
os.chdir(r'../')

from MainFlask import quepySender


class BaseTestClass(unittest.TestCase):
    def test_initial_query(self):
        input = "Who is Donald Trump?"
        print("quepy result test: ", quepySender(input))


if __name__ == '__main__':
    unittest.main()