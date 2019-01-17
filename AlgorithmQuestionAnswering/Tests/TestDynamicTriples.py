import unittest
import os
os.chdir(r'../')

import Utils
from SPARQLGenerator import SPARQLGeneratorClass




class BaseTestClass(unittest.TestCase):
    def test_dynamic_average_question_type_one(self):
        statement = "Could you tell me what is average for sensor3 in machine3?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        result_selenium = SPARQLGeneratorClass.queryTestingSelenium(queryLinkedFactory)
        self.assertEqual(result_selenium.get('avg'), '6.33333')

    def test_dynamic_average_indicative_question(self):
        statement = "I need to learn an average for sensor1 in machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        result_selenium = SPARQLGeneratorClass.queryTestingSelenium(queryLinkedFactory)
        self.assertEqual(result_selenium.get('avg'), '6.33333')


    #@unittest.skip("Last query will be tested")
    def test_dynamic_average_question_type_two(self):
        statement = "What is the average of sensor3 in machine3?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        result_selenium = SPARQLGeneratorClass.queryTestingSelenium(queryLinkedFactory)
        self.assertNotEqual(result_selenium.get('avg'), '6.33333')

if __name__ == '__main__':
    unittest.main()
