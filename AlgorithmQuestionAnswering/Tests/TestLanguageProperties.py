import unittest
import spacy
nlp = spacy.load('en_core_web_md')

class SpacyEvaluation():
    #spacy detects noun chunks
    def detect_noun_chunk(self, phrase):
        doc = nlp(phrase)
        print(list(doc.noun_chunks))
        for noun_phrase in list(doc.noun_chunks):
            noun_phrase.merge(noun_phrase.root.tag_, noun_phrase.root.lemma_, noun_phrase.root.ent_type_)
            print("noun phrase", noun_phrase)

class BaseTestClass(unittest.TestCase):
    def test_detect_noun_chunk(self):
        spacy_evaluation = SpacyEvaluation()
        spacy_evaluation.detect_noun_chunk("What does linkedfactory contain?")

if __name__ == '__main__':
    unittest.main()