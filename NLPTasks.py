#This py file will use Stanford Core NLP Server
from collections import defaultdict

from stanfordcorenlp import StanfordCoreNLP
import json
import logging
import colored_logs, AppLogger

class testConnectionCoreNLP(object):
    def __init__(self, host="http://localhost", port=9000):
        self.nlp = StanfordCoreNLP(host, port=port, timeout=3000) # quiet = False, logging_level = logging.DEBUG

        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage' : 'en',
            'outputFormat' : 'json'
        }

    def word_tokenize(self, sentence):
        AppLogger.log.info("word tokenize")
        return self.nlp.word_tokenize(sentence)

    def posTagger(self, sentence):
        AppLogger.log.info("pos tagger")
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        AppLogger.log.info("ner")
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        AppLogger.log.info("parser activated")
        return self.nlp.parse(sentence)

    def dependency_parser(self, sentence):
        AppLogger.log.info("dependency parser activated")
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        AppLogger.log.info("annotator")
        return json.loads(self.nlp.annotate(sentence, properties=self.props))

    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                'word' : token['word']
            }


nlpCore = testConnectionCoreNLP()
TestInput = 'A blog post using Stanford CoreNLP Server. Visit www.khalidalnajjar.com for more details.'
print('Tokenize', nlpCore.word_tokenize(TestInput))
print('Part of Speech Tagger', nlpCore.posTagger(TestInput))
print('Named Entities', nlpCore.ner(TestInput))
print('Constituency Parsing:', nlpCore.parse(TestInput))
print('Dependency Parsing', nlpCore.dependency_parser(TestInput))
#Tested with Server. Stanford CoreNLP server up and running