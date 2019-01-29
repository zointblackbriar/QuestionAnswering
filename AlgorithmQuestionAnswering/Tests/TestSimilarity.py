import unittest
import os
os.chdir(r'../')
import StanfordSpacyNLP

#corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()



class BaseTestClass(unittest.TestCase):

    #wordnet similarity gives us a best matched for lemmatized verb
    def test_similarity_wordnet(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.wordnetLatentAnalysis("incorporate", "contains")
        self.assertTrue(result)

    def test_similarity_leventshein(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_word_levensthein("incorporate", "contains")
        self.assertTrue(result)

    def test_jaro_winkler(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_jaro_winkler("incorporate", "contains")
        self.assertTrue(result)

    def test_jaro_winkler_third(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_jaro_winkler("comprise", "contains")
        self.assertTrue(result)

    def test_jaro_winkler_fourth(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_jaro_winkler("holds", "contains")
        self.assertTrue(result)

    def test_jaro_winkler_fifth(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_jaro_winkler("hold back", "contains")
        self.assertTrue(result)

    def test_jaro_winkler_second(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_jaro_winkler("graze", "contains")
        self.assertFalse(result)

    def test_levensthein_sentence_similarity_1(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_levenshtein("Is the system health good?", "system health for sensor2 in machine6?")
        self.assertTrue(result)

    def test_levensthein_sentence_similarity_2(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_levenshtein("Is the system health good for sensor1 belongs to machine1?", "Could you tell me the system health for sensor2 in machine1?")
        self.assertTrue(result)

    def test_levensthein_sentence_similarity_3(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_levenshtein("Is the system health good?", "health for sensor1 in machine2")
        self.assertTrue(result)

    def test_levensthein_sentence_similarity_4(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_levenshtein("Is the system health good?", "Is the system health good?")
        self.assertTrue(result)

    def test_levensthein_sentence_similarity_5(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_levenshtein("Is the system health good for sensor1 in machine1?", "health for sensor1 in machine2")
        self.assertTrue(result)

    def test_levensthein_sentence_similarity_6(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_levenshtein("Is the system health good for sensor1 of machine1?", "Could you tell me the system health for sensor2 in machine1?")
        self.assertTrue(result)

    def test_levensthein_sentence_similarity_7(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.similarity_levenshtein("Is the system health bad for sensor1 within machine1?", "Could you tell me the system health for sensor5 in machine3?")
        self.assertTrue(result)



if __name__ == '__main__':
    unittest.main()
