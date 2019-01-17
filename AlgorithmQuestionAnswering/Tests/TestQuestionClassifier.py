import os
os.chdir(r'../')

import unittest
from QuestionClassification.QuestionClassifier import QuestionAssigner
from sklearn.externals import joblib


clf = joblib.load('model/LogisticRegressionNew.pkl')

class BaseTestClass(unittest.TestCase):

    def test_what_question_classification(self):
        statement = "What is the value of sensor1 in machine1?"
        self.assertEqual(QuestionAssigner.predictQuestion(statement), 'what')

    def test_when_question_classification(self):
        statement = "When is lowest value of sensor1 in machine1"
        self.assertEqual(QuestionAssigner.predictQuestion(statement), 'when')

    def test_affirmative_sentence_classification(self):
        statement = "Give me the value of sensor1 in machine1"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

    def test_how_question_classification(self):
        statement = "How contains linkedfactory?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'how')

    def test_how_question_classification_second(self):
        statement = "how do you spell?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'how')

    def test_question_1(self):

        statement = "What is the value of sensor1 in machine1?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'what')

    #What incorporates rollex
    def test_question_2(self):

        statement = "Would you give me what does rollex incorporate?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

    def test_question_3(self):
        statement = "What incorporates rollex?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'what')

    def test_question_4(self):
        statement = "Could you give me average of sensor1 in machine1?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')


    def test_question_5(self):
        statement = "What contains ha100?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'what')

    def test_question_6(self):
        statement = "Give me the name of Stations in generated data?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

    def test_question_7(self):
        statement = "Who is the value of sensor1 in machine1?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'who')

    def test_question_8(self):
        statement = "Could you give me parent node id in the file of generated data?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

    def test_question_9(self):
        statement = "I need to learn parent node id in generated data"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

    def test_question_10(self):
        statement = "Who is the value of sensor1 in machine1?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'who')

    def test_question_11(self):
        statement = "Give me all registered node id?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'what')

    def test_question_12(self):
        statement = "Could you give me parent node id in the file of generated data?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

    def test_question_13(self):
        statement =  "Give me all data blocks?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'what')

    def test_question_14(self):
        statement = "data blocks in generated OPC file?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

    def test_question_15(self):
        statement = "data blocks in generated OPC file?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

    def test_question_16(self):
        statement = "All station which is in generated data or new data?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

    def test_question_17(self):
        statement =  "Give me the name of Stations in generated data?"
        result = QuestionAssigner.predictQuestion(statement)
        self.assertEqual(result, 'affirmation')

if __name__ == '__main__':
    unittest.main()