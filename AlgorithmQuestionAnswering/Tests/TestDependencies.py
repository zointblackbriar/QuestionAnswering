import unittest
import StanfordSpacyNLP


class BaseTestClass(unittest.TestCase):

    def test_first_dependency(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        self.assertTrue(corenlpObject.spacyDependencyChunk("What contains fofab?"))

    def test_second_dependency(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        self.assertFalse(corenlpObject.spacyDependencyChunk("What does linkedfactory contain?"))

    def test_third_dependency(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        self.assertTrue(corenlpObject.spacyDependencyChunk("Could you give me please what contains linkedfactory?"))


    def test_fourth_dependency(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        self.assertFalse(corenlpObject.spacyDependencyChunk("Would you give me what does rollex incorporate?"))


    def test_fifth_dependency(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        self.assertFalse(corenlpObject.spacyDependencyChunk("I need you to tell me which one contained by linkedfactory"))

    def test_sixth_dependency(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        self.assertFalse(corenlpObject.spacyDependencyChunk("What linkedfactory contains?"))

    def test_keyword_dependency(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        self.assertFalse(corenlpObject.spacyDependencyChunk("linkedfactory contains"))





if __name__ == '__main__':
    unittest.main()
