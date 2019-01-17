import StanfordSpacyNLP
import json, ast
import unittest
from NLTKProp import NLTKProp
from pattern.text.en import singularize


class BaseTestClass(unittest.TestCase):


    """test for questions"""
    def test_sentence_dependency_parse_test(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        sentence = "What linkedfactory contains?"
        tree = corenlpObject.constituencyParser(sentence)
        print(corenlpObject.findVPSubtree(tree))
        value = ast.literal_eval(json.dumps(corenlpObject.findVPSubtree(tree)[0]))
        self.assertEqual(value, 'contains')
        self.assertTrue(corenlpObject.wordnetLatentAnalysis(value, "contains"))

    def test_dependency_parse_tree_output(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()

        self.assertIsInstance(corenlpObject.dependencyParser("What incorporates rollex?"), list)
        self.assertEqual(corenlpObject.dependencyParser("What incorporates rollex?"), [(u'ROOT', 0, 2), (u'nsubj', 2, 1), (u'dobj', 2, 3), (u'punct', 2, 4)])
        self.assertEqual(corenlpObject.dependencyParser("What incorporates rollex?")[1], (u'nsubj', 2, 1))
        #self.assertEqual(corenlpObject.dependencyParser("What rollex incorporates"), [(u'ROOT', 0, 2), (u'nsubj', 2, 1), (u'dobj', 2, 3), (u'punct', 2, 4)])
        self.assertEqual(corenlpObject.dependencyParser("Would you give me what does rollex incorporates"), [(u'ROOT', 0, 3), (u'aux', 3, 1), (u'nsubj', 3, 2), (u'dobj', 3, 4), (u'dobj', 8, 5), (u'aux', 8, 6), (u'nsubj', 8, 7), (u'ccomp', 3, 8)])
        self.assertEqual(corenlpObject.dependencyParser("What does rollex contain?"), corenlpObject.dependencyParser("What incorporates rollex?"))

    def test_named_entity_recognition(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()

        input = "What is the value of sensor1 in machine1 between 11/6/2018-16.58 and 11/6/2018-17.59"
        self.assertEqual(corenlpObject.namedEntityRecognition(input), None)

    def test_spacy_dependency_parser(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()

        input = "What does linkedfactory incorporate?"
        self.assertEqual(corenlpObject.spacyDependencyParser(input), [{u'modifiers': [{u'modifiers': [], u'word': u'What', u'NE': u'', u'POS_coarse': u'NOUN', u'lemma': u'what', u'arc': u'dobj', u'POS_fine': u'WP'}, {u'modifiers': [], u'word': u'does', u'NE': u'', u'POS_coarse': u'VERB', u'lemma': u'do', u'arc': u'aux', u'POS_fine': u'VBZ'}, {u'modifiers': [], u'word': u'linkedfactory', u'NE': u'', u'POS_coarse': u'NOUN', u'lemma': u'linkedfactory', u'arc': u'nsubj', u'POS_fine': u'NN'}, {u'modifiers': [], u'word': u'?', u'NE': u'', u'POS_coarse': u'PUNCT', u'lemma': u'?', u'arc': u'punct', u'POS_fine': u'.'}], u'word': u'contain', u'POS_coarse': u'VERB', u'arc': u'ROOT', u'POS_fine': u'VB'}])

    def test_spacy_verb_lemmatization(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()

        input = "What contains linkedfactory?"
        verb = corenlpObject.spacyArchMatching(input)
        self.assertEqual(corenlpObject.spacy_verb_lemmatizer(str(verb[0])), u'contain')

    def test_spacy_noun_lemmatization(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()

        input = "What contains linkedfactories?"
        constituent_parse = corenlpObject.constituencyParser(input)
        noun = corenlpObject.findNNSubtree(constituent_parse)
        self.assertEqual(corenlpObject.spacy_noun_lemmatizer(str(noun)), u'linkedfactory')

    def test_spacy_noun_stemming(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        nltk_object   = NLTKProp()
        input = "What contains linkedfactories?"
        constituent_parse = corenlpObject.constituencyParser(input)
        noun = corenlpObject.findNNSubtree(constituent_parse)
        self.assertEqual(nltk_object.stemmingPorter(str(noun)), u'linkedfactory')

    def test_singularize_noun(self):
        corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()
        #nltk_object = NLTKProp()
        input = "What contains linkedfactories and fofabs?"
        constituent_parse = corenlpObject.constituencyParser(input)
        noun = corenlpObject.findNNSubtree(constituent_parse)
        singles = [singularize(plural) for plural in noun]
        print("type of singles", type(singles))
        self.assertEqual(singles, u'linkedfactory')



if __name__ == '__main__':
    unittest.main()

