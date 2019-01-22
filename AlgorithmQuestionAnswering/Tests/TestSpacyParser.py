import unittest
import StanfordSpacyNLP
from StanfordSpacyNLP import TestConnectionCoreNLP
import NLTKProp


corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()


class BaseTestClass(unittest.TestCase):

    # def testFailedDependencyParser(self):
    #     self.assertEqual(corenlpObject.spacyDetailedDependencyChunk("What is the value of sensor1 in machine1?"), [u'attr', u'nsubj', u'pobj', u'pobj'])
    #
    # def testCorrectedDependencyParser(self):
    #     self.assertEqual(corenlpObject.spacyDetailedDependencyChunk("What is the value of sensor1 in machine1?"), [u'attr', u'nsubj', u'pobj', u'pobj'])
    #
    # def testAffirmationQuestionDependencyParser(self):
    #     self.assertEqual(corenlpObject.spacyDetailedDependencyChunk("Give me all the members of linkedfactory ?"), [u'dative', u'dobj', u'pobj'])
    #
    # def testInversedQuestion(self):
    #     self.assertEqual(corenlpObject.spacyDetailedDependencyChunk("What contains ha100?"), [u'nsubj'])
    #
    # def testAffirmativeQuestion(self):
    #     self.assertEqual(corenlpObject.spacyDetailedDependencyChunk("Could you give me the value that linkedfactory contains ?"), [u'nsubj', u'dative', u'dobj', u'nsubj'])
    #
    # def testDynamicQuestion(self):
    #     self.assertEqual(corenlpObject.spacyDetailedDependencyChunk("What is the value of sensor3 in machine3?"), [u'attr', u'nsubj', u'pobj', u'pobj'])
    #
    # def testDataFrameDependencyRelations(self):
    #     self.assertEqual(corenlpObject.spacyDependencyRelations("What is the value of sensor1 in machine1?"), [u'VERB', u'VERB', u'NOUN', u'VERB', u'NOUN', u'ADP', u'NOUN', u'ADP', u'VERB'])

    # def testDynamicMatchingArc(self):
    #     statement = "What is the value of sensor1 in machine1?"
    #     verbs = corenlpObject.spacyArchMatching(statement)
    #     print(type(verbs))
    #     print(verbs[-1])
    #     self.assertEqual(str(verbs[0]), 'is')
    #
    # def testStaticMatchingArc(self):
    #     statement = "Could you give me the value of sensor1 in machine1?"
    #     verbs = corenlpObject.spacyArchMatching(statement)
    #     self.assertEqual(str(verbs[0]), 'give')
    #
    # def testStraightMatchingArc(self):
    #     statement = "Could you give me the value that linkedfactory contains ?"
    #     self.expected = ['give', 'contains']
    #     self.actual = corenlpObject.spacyArchMatching(statement)
    #     self.assertEqual(type(self.actual), type(self.expected))
    #     self.assertEqual(type(self.expected), "<type 'list'>")
    #     self.assertListEqual(self.actual, self.expected)
    #
    # def testSpacyDependencyChunk(self):
    #     statement = "What contains linkedfactory?"
    #     self.assertTrue(corenlpObject.spacyDependencyChunk(statement))
    #
    # def testSpacyInverseVersion1DependencyChunk(self):
    #     statement = "What does linkedfactory contains?"
    #     self.assertFalse(corenlpObject.spacyDependencyChunk(statement))
    #

    @unittest.skip("Dependency chunk will be tested")
    def test_SpacyInverseVersion2DependencyChunk(self):
        statement = "Could you give me the members in which contained by linkedfactory?"
        self.assertFalse(corenlpObject.spacyDependencyChunk(statement))

    @unittest.skip("Dependency chunk will be tested")
    def test_SpacyInverseVersion3DependencyChunk(self):
        statement = "Which one incorporates linkedfactory show me please? "
        self.assertTrue(corenlpObject.spacyDependencyChunk(statement))

    @unittest.skip("Dependency chunk will be tested")
    def test_SpacyCoreferenceResolution(self):
        statement = "My sister has a dog. She loves him"
        self.assertTrue(corenlpObject.spacyCoreferenceResolution(statement))

    @unittest.skip("Dependency chunk will be tested")
    def test_SpacyOurCaseCoreferenceResolution(self):
        statement = "Keep that in mind. What is the value of sensor1 in machine1"
        self.assertTrue(corenlpObject.spacyCoreferenceResolution(statement))

    @unittest.skip("Dependency chunk will be tested")
    def test_SpacyInverseQueryChunkTagger(self):
        statement = "What contains IWU?"
        self.assertEqual(corenlpObject.spacyDetailedDependencyChunk(statement), [u'nsubj', u'dobj'])

    @unittest.skip("Dependency chunk will be tested")
    def test_SpacyInverseQueryPosTagger(self):
        statement = "What contains IWU?"
        self.assertEqual(corenlpObject.spacyDependencyRelations(statement), "hello")

    @unittest.skip("Dependency chunk will be tested")
    def test_textBlob(self):
        statement = "What contains IWU?"
        self.assertEqual(corenlpObject.textblobPatternParser(statement), "hello")

    def test_spacyDependencyChunk_first(self):
        statement = "What contains IWU?"
        self.assertTrue(corenlpObject.spacyDependencyChunk(statement))

    def test_spacyDependencyChunk_second(self):
        statement = "Could you give me What contains linkedfactory?"
        self.assertTrue(corenlpObject.spacyDependencyChunk(statement))

    def test_spacyDependencyChunk_third(self):
        statement = "Could you give me which one contains linkedfactory?"
        self.assertTrue(corenlpObject.spacyDependencyChunk(statement))

    def test_direct_question(self):
        statement = "What linkedfactory contains?"
        self.assertFalse(corenlpObject.spacyDependencyChunk(statement))

    def test_indirect_question(self):
        statement = "What contains Aximus?"
        self.assertTrue(corenlpObject.spacyDependencyChunk(statement))


    def test_a_query(self):
        statement = "What does linkedfactory contain?"
        self.assertFalse(corenlpObject.spacyDependencyChunk(statement))

    # def test_spacy_lemmatizer(self):
    #     statement = "What contains linkedfactory?"
    #     nlpTask = TestConnectionCoreNLP()
    #     verb = nlpTask.spacyArchMatching(statement)
    #     self.assertEqual(corenlpObject.spacy_lemmatizer(verb), 'contain')


    # def test_StanfordCoreferenceResolution(self):
    #     statement = "What is the value of sensor1 in machine1?"
    #     corenlpObject.stanfordCoreferenceResolution(statement)

    # def test_StanforCoreRefenceResolution(self):
    #     statement = "What is the value of sensor1 in machine1?"
    #     self.assertEqual(corenlpObject.coreferenceSolutionStanford(statement), "hello")

if __name__ == '__main__':
    unittest.main()