import numpy as np
import os
os.chdir(r'../')

import unittest


class Vectorization():
    def get_all_data_w2v(self):
        with open("glove/glove.6B.50d.txt", "r+") as lines:
            #assign to a dictionary
            w2v = {line.split()[0]: np.array(map(float, line.split()[1:])) for line in lines}
            print(w2v)


class BaseTestClass(unittest.TestCase):
    def test_data_fetch(self):
        vector = Vectorization()
        vector.get_all_data_w2v()

if __name__ == '__main__':
    unittest.main()