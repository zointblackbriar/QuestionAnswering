#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

#This py file will use Stanford Core NLP Server
from collections import defaultdict

import nltk
from nltk.corpus import wordnet
from itertools import chain
from stanfordcorenlp import StanfordCoreNLP
import json
import logging
from nltk.tree import *

logger = logging.getLogger(__name__)

class ConnectionCoreNLP(object):
    def __init__(self, host="http://localhost", port=9000):
        self.nlp = StanfordCoreNLP(host, port=port, timeout=3000) # quiet = False, logging_level = logging.DEBUG

        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage' : 'en',
            'outputFormat' : 'json'
        }

    def word_tokenize(self, sentence):
        logger.info("word tokenize")
        return self.nlp.word_tokenize(sentence)

    def posTagger(self, sentence):
        logger.info("pos tagger")
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        logger.info("ner")
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        logger.info("parser activated")
        return self.nlp.parse(sentence)

    def dependency_parser(self, sentence):
        logger.info("dependency parser activated")
        return self.nlp.dependency_parse(sentence)

    def deterministic_coreference(self, sentence):
        logger.info("deterministic coreference activated")
        return self.nlp.coref(sentence)

    def annotate(self, sentence):
        logger.info("annotator")
        return json.loads(self.nlp.annotate(sentence, properties=self.props))

    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                'word' : token['word']
            }

nlpCore = ConnectionCoreNLP()

class TestConnectionCoreNLP(object):
    # print('Tokenize', nlpCore.word_tokenize(param_test))
    # print('Part of Speech Tagger', nlpCore.posTagger(param_test))
    # print('Named Entities', nlpCore.ner(param_test))
    # print('ner list: ', param_test)
    def __init__(self):
        pass

    def dependencyParser(self, param_depend):
        try:
            # print('Dependency Parsing:', nlpCore.parse(param_depend))
            dependencyParseTree = nlpCore.dependency_parser(param_depend)
            print(dependencyParseTree)
            #be careful when you return dependencyParseTree
            #It is not a tree
            #It is a unicoded string format
            #return Tree.fromstring(dependencyParseTree)
        except Exception as ex:
            logger.exception("Dependency Parser Error")

        #Tested with Server. Stanford CoreNLP server up and running
    def constituencyParser(self, param_constituent):
        try:
            constituentParseTree = nlpCore.parse(param_constituent)
            # print(constituentParseTree)
            return Tree.fromstring(constituentParseTree)
        except Exception as ex:
            logger.exception("Constituency Parser error")

    #Find tree's node with the following method
    #get_node function has been changed with label() function
    def printSubtrees(self, tree, constituentTags, extraCheckTags):
        try:
            for subtree in tree.subtrees():
                if subtree.label() == constituentTags or subtree.label() == extraCheckTags:
                    return subtree.leaves()
        except Exception as e:
            logger.exception("Subtree parse problem")

    def findSpecificSubtree(self, tree):
        #print("tree find specific", tree)
        try:
            NPs = list(tree.subtrees(filter=lambda x: x.label() == 'NP'))
            NNs_insideNPs = map(lambda x: list(x.subtrees(filter=lambda x: x.label() == 'NN')), NPs)
            return self.removeDuplicates([noun.leaves()[0] for nouns in NNs_insideNPs for noun in nouns])
        except Exception as ex:
            logger.exception("Constituency Parser error")

    def removeDuplicates(self, dup_list):
        assignmentList = []
        for elem in dup_list:
            if elem not in assignmentList:
                assignmentList.append(elem)
        return assignmentList

    #Write all nodes of NLTK Parse Tree
    #This function has some errors it should be fixed.
    def getNodes(self, tree):
        output = []
        try:
            for node in tree:
                if type(node) is nltk.Tree:
                    if node.label() == 'ROOT':
                        print("=====Sentence=====")
                        print("Sentence:", ".join(node.leaves()")
                    elif node.label() == 'NN':
                        #append all the nodes into the list of python
                        output.append(node.leaves())
                    else:
                        print("Label:", node.label())
                        print("Leaves", node.leaves())
                    #print("output", output)
                    self.getNodes(node)

        except Exception as ex:
                logger.exception("Get node function couldn't parse it")
        yield output

    #with pure nltk to find synonym
    def synonym(self, input):
        synonyms = wordnet.synsets(input)
        lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
        print(lemmas)

    #n-grams function in NLP
    #if you want to do bigram, please send a value n=2
    #Usage is self.ngrams("What is the value of sensor1 in machine1".split(), 2]
    def ngrams(self, words, n):
        return [words[i:i+n] for i in range(len(words)-n+1)]


    #Wordnet Latent Semantic Analysis - To test for synonyms
    def simulation(self, word1, word2, lch_threshold=2.15, verbose=False):
        """Determine if two (already lemmatized) words are similar or not"""

        """Call with verbose=True to print the Wordnet senses from each word that are considered similar"""

        from nltk.corpus import wordnet as wn
        results = []
        for net1 in wn.synsets(word1):
            for net2 in wn.synsets(word2):
                try:
                    lch = net1.lch_similarity(net2)
                except:
                    continue
                #The value to compare the LCH to was found empirically
                #The value is application dependent. Do experiment
                if lch >= lch_threshold:
                    results.append((net1, net2))
        if not results:
            return False
        if verbose:
            for net1, net2 in results:
                print(net1)
                print(net1.definition)
                print(net2)
                print(net2.definition)
                print('path similarity')
                print(net1.path_similarity(net2))
                print(net1.lch_similarity(net2))
                print('wup similarity:')
                print(net1.wup_similarity(net2))
                print('-' + 79)
        return True

