import unittest
import StanfordSpacyNLP

class BaseTestCase(unittest.TestCase):

    @unittest.skip("Don't test jaccard")
    def test_jaccard_second_similarity(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement_first = "Is everthing ok?"
        statement_second = "Give me the status of system health"
        self.assertTrue(obj.similarity_jaccard(statement_first, statement_second))

    @unittest.skip("Don't test jaccard")
    def test_jaccord_third_similarity(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement_first = "Is the system health good?"
        statement_second = "System health status"
        self.assertTrue(obj.similarity_jaccard(statement_first, statement_second))

    def test_jaccord_similarity(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement_first = "Is the system health good?"
        statement_second = "How is it going on system health?"
        self.assertTrue(obj.similarity_jaccard(statement_first, statement_second))


    def test_jaro_winkler(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement_first = "Is the system health good?"
        statement_second = "How is it going on system health?"
        self.assertTrue(obj.similarity_jaro_winkler(statement_first, statement_second))

    def test_levenshtein(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement_first = "Is the system health good?"
        statement_second = "How is it going on system health?"
        self.assertTrue(obj.similarity_levenshtein(statement_first, statement_second))

    def test_jaccord__browse(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement_first = "Could you browse generated data?"
        statement_second = "Can you browse for me on generated data?"
        self.assertTrue(obj.similarity_jaccard(statement_first, statement_second))


    def test_jaro_winkler_browse(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement_first = "Could you browse generated data?"
        statement_second = "Can you browse for me on generated data?"
        self.assertTrue(obj.similarity_jaro_winkler(statement_first, statement_second))

    def test_levenshtein_browse(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement_first = "browse generated data?"
        statement_second = "Can you browse for me on generated data?"
        self.assertTrue(obj.similarity_levenshtein(statement_first, statement_second))


    def test_sentence_first_positivity(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement = "Could you browse all nodes?"
        statementFlag = obj.textblob_sentiment_analysis(statement)
        self.assertTrue(statementFlag)

    def test_sentence_second_positivity(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement = "Can you browse all nodes?"
        statementFlag = obj.textblob_sentiment_analysis(statement)
        self.assertTrue(statementFlag)

    def test_sentence_third_positivity(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement = "I am happy"
        statementFlag = obj.textblob_sentiment_analysis(statement)
        self.assertTrue(statementFlag)

    def test_sentence_fourth_positivity(self):
        obj = StanfordSpacyNLP.TestConnectionCoreNLP()
        statement = "Don't give me the value of sensor1 in machine1"
        statementFlag = obj.textblob_sentiment_analysis(statement)
        self.assertFalse(statementFlag)


if __name__ == '__main__':
    unittest.main()