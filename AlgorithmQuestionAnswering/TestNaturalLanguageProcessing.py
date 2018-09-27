import unittest
from NaturalLanguageProcessing import *

obj = NaturalProcess

class MyTest(unittest.TestCase):
    def testFrequencyWords(self):
        param_input = "My name is Orcun"
        print(obj.wordFrequencyCount(obj, param_input))
        #assert(obj.wordFrequencyCount(self, param_input), 5)
