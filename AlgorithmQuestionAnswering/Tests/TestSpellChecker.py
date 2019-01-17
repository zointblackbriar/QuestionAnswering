import unittest
import os
os.chdir(r'../')

from StanfordSpacyNLP import TestConnectionCoreNLP
from spellchecker import SpellChecker
import textacy
import nltk
import re
from collections import Counter


def words(text): return re.findall(r'\w+', text.lower())


WORDS = Counter(words(open('data/big.txt').read()))


class BaseClass(unittest.TestCase):
    #this gives us an error because of python version. It support python version 3
    @unittest.skip("library is not working")
    def test_spell_checker_words(self):
        speller = SpellChecker()
        mispelled = speller.unknown(['let', 'us', 'wlak', 'on', 'the', 'groun'])

        for word in mispelled:
            print("speller correction:", speller.correction(word))

            print("speller likely options", speller.candidates)

    @unittest.skip("function is wrong")
    def test_currency_abbreviation_textacy(self):
        input = "Hello give me a loads of USD."
        result = nltk.word_tokenize(input)
        print("result list", result)
        for word in result:
            print(textacy.preprocess.replace_currency_symbols(word))

    def test_spell_correction_norvig_algorithm(self):
        input = "I don't know how to speling."
        obj = SpellCorrection()
        result = nltk.word_tokenize(input)
        for word in result:
            print(obj.correction(word))

    def test_spell_correction_norvig_algorithm_abbreviation(self):
        input = "What's the value of linkedfactory"
        obj = SpellCorrection()
        result = nltk.word_tokenize(input)
        for word in result:
            print(obj.correction(word))

    def test_spell_correction_norvig_algorithm_abbreviation_etc(self):
        input = "I won't have it."
        obj = SpellCorrection()
        result = nltk.word_tokenize(input)
        for word in result:
            print(obj.correction(word))

    def test_spell_correction_norvig_algorithm_abbreviation_abbr_dict(self):
        abbr_dict = [
            "what's",
            "what're",
            "who's",
            "who're",
            "where's",
            "where're",
            "when's",
            "when're",
            "how's",
            "how're",
            "i'm",
            "we're",
            "you're",
            "they're",
            "it's",
            "he's",
            "she's",
            "that's",
            "there's",
            "there're",
            "i've",
            "we've",
            "you've",
            "they've",
            "who've",
            "would've",
            "not've",
            "i'll",
            "we'll",
            "you'll",
            "he'll",
            "she'll",
            "it'll",
            "they'll",
            "isn't",
            "wasn't",
            "aren't",
            "weren't",
            "can't",
            "couldn't",
            "don't",
            "didn't",
            "shouldn't",
            "wouldn't",
            "doesn't",
            "haven't",
            "hasn't",
            "hadn't",
            "won't"
        ]

        obj = SpellCorrection()
        for word in abbr_dict:
            print(obj.correction(word))




class SpellCorrection:

    def P(self, word, N=sum(WORDS.values())):
        "Probability of `word`."
        return WORDS[word] / N

    def correction(self, word):
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.P)

    def candidates(self, word):
        "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in WORDS)

    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


if __name__ == '__main__':
    unittest.main()
