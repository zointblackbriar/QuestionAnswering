import unittest
import logging
from NLTKProp import NLTKProp
from StanfordSpacyNLP import TestConnectionCoreNLP
import time

logger = logging.getLogger(__name__)



class BaseTestClass(unittest.TestCase):
    def test_sentiment_analysis(self):
        logger.info("test_sentiment_analysis")
        import StanfordSpacyNLP
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement = "Don't give me the value of sensor1 in machine1?"
        self.assertFalse(corenlpObject.textblob_sentiment_analysis(statement))

    def test_snowball_stemmer(self):
        logger.info("test_snowball_stemmer")
        statement = ['What contains linkedfactory?', 'What does linkedfactory contain?']
        testverb = []
        nlpTask = TestConnectionCoreNLP()
        testverb.append(nlpTask.spacyArchMatching(statement[0]))
        testverb.append(nlpTask.spacyArchMatching(statement[1]))
        print(testverb[0])
        print(testverb[1])
        self.assertEqual(NLTKProp.stemmingSnowball(str(testverb[0])), "contains")
        self.assertEqual(NLTKProp.stemmingSnowball(str(testverb[1])), "contains")

    @unittest.skip("Snowball Stemmer will be tested")
    def test_porter_stemmer(self):
        logger.info("test_porter_stemmer")
        statement = ['What contains linkedfactory?', 'What does linkedfactory contain?']
        self.assertEqual(NLTKProp.stemmingPorter(statement[0]), "contains")
        self.assertEqual(NLTKProp.stemmingPorter(statement[1]), "contains")


if __name__ == 'main':
    unittest.main()