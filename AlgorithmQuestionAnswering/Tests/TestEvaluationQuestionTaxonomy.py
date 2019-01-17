# -*- coding: utf-8 -*-


import unittest
import os
os.chdir(r'../')
import Utils
from SPARQLGenerator import SPARQLGeneratorClass
from time import time
import spacy

"""
The following questions have been taken from a list in the book named Speech and Language Processing Jurafsky, Daniel; Martin, James H

ABBREVIATION 
What’s the abbreviation for limited partnership?
What does the "c" stand for in the equation E=mc2?
DESCRIPTION
What are tannins?
What are the words to the Canadian National anthem?
How can you get rust stains out of clothing?
What caused the Titanic to sink?
ENTITY
What are the names of Odin’s ravens?
What part of your body contains the corpus callosum?
What colors make up a rainbow?
In what book can I find the story of Aladdin?
What currency is used in China?
What does Salk vaccine prevent?
What war involved the battle of Chapultepec?
What kind of nuts are used in marzipan?
What instrument does Max Roach play?
What’s the official language of Algeria?
What letter appears on the cold-water tap in Spain?
What is the name of King Arthur’s sword?
What are some fragrant white climbing roses?
What is the fastest computer?
What religion has the most members?
What was the name of the ball game played by the Mayans?
What fuel do airplanes use?
What is the chemical symbol for nitrogen?
What is the best way to remove wallpaper?
How do you say “ Grandma” in Irish?
What was the name of Captain Bligh’s ship?
What’s the singular of dice?
HUMAN
Who was Confucius?
What are the major companies that are part of Dow Jones?
Who was the first Russian astronaut to do a spacewalk?
What was Queen Victoria’s title regarding India?
LOCATION 
What’s the oldest capital city in the Americas?
What country borders the most others?
What is the highest peak in Africa?
What river runs through Liverpool?
What states do not have state income tax?
NUMERIC
What is the telephone number for the University of Colorado?
About how many soldiers died in World War II?
What is the date of Boxing Day?
How long was Mao’s 1930s Long March?
How much did a McDonald’s hamburger cost in 1963?
Where does Shanghai rank among world cities in population?
What is the population of Mexico?
What was the average life expectancy during the Stone Age?
What fraction of a beaver’s life is spent swimming?
How hot should the oven be when making Peachy Oat Muffins?
How fast must a spacecraft travel to escape Earth’s gravity?
What is the size of Argentina?
How many pounds are there in a stone?
"""

from QuestionClassification import QuestionClassificationSVM
EN_MODEL_MD = "en_core_web_md"
nlp_loader = spacy.load(EN_MODEL_MD)


class BaseTestClass(unittest.TestCase):

    def test_question_1(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "What is the value of sensor1 in machine1?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'DESC')

    #What incorporates rollex
    def test_question_2(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Would you give me what does rollex incorporate?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'DESC')

    def test_question_3(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc1 = nlp_loader(u'' + "What incorporates rollex?")
        self.assertEqual(classification_object.classify_question(doc1)[0], 'DESC')

    def test_question_4(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Could you give me average of sensor1 in machine1?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'DESC')

    def test_question_5(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "What contains ha100?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'DESC')

    def test_question_6(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Give me the name of Stations in generated data?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'DESC')

    def test_question_7(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Who is the value of sensor1 in machine1?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_8(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Could you give me parent node id in the file of generated data?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_9(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "I need to learn parent node id in generated data")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_10(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Who is the value of sensor1 in machine1?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_11(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Give me all registered node id?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_12(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Could you give me parent node id in the file of generated data?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_13(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Give me all data blocks?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_14(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "data blocks in generated OPC file?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_15(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "data blocks in generated OPC file?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_16(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "All station which is in generated data or new data?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')

    def test_question_17(self):
        classification_object = QuestionClassificationSVM.SVMClassifier()
        doc = nlp_loader(u'' + "Give me the name of Stations in generated data?")
        self.assertEqual(classification_object.classify_question(doc)[0], 'HUM')


if __name__ == '__main__':
    unittest.main()
