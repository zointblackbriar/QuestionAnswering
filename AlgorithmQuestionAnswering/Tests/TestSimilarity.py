import unittest
import os
os.chdir(r'../')
import StanfordSpacyNLP

corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()



class BaseTestClass(unittest.TestCase):

    #wordnet similarity gives us a best matched for lemmatized verb
    def test_similarity_wordnet(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        result = corenlpObject.wordnetLatentAnalysis("incorporate", "contains")
        self.assertTrue(result)

    @unittest.skip("leventshein skip")
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


if __name__ == '__main__':
    unittest.main()
