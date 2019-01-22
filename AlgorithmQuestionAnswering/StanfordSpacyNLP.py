#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

# try:
#     unicode_ = unicode #Python2
# except NameError:
#     unicode_ = str #Python3


#This py file will use Stanford Core NLP Server
from collections import defaultdict

import nltk
from textblob import TextBlob
from textblob.parsers import PatternParser
from nltk.corpus import wordnet
from nltk import word_tokenize
from itertools import chain
from stanfordcorenlp import StanfordCoreNLP
from textblob.sentiments import NaiveBayesAnalyzer
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from textacy import similarity

import json
import logging
from nltk.tree import *
import spacy
import pandas as pd
from spacy.symbols import  *

#import en_coref_md
import en_coref_lg

logger = logging.getLogger(__name__)

class ConnectionCoreNLP(object):
    def __init__(self, host="http://localhost", port=9000):
        self.nlp = StanfordCoreNLP(host, port=port, timeout=30000) # quiet = False, logging_level = logging.DEBUG
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation','sentiment'
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
                'word' : token['word'],
                'lemma' : token['lemma'],
                'pos' : token['pos'],
                'ner' : token['ner']
            }
        return tokens

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
            dependencyParseTree = nlpCore.dependency_parser(param_depend)
            #be careful when you return dependencyParseTree
            #It is not a tree
            #It is a unicoded string format
        except Exception as ex:
            logger.exception("Dependency Parser Error")
        return dependencyParseTree

    def coreferenceSolutionStanford(self, sentence):
        coreference = nlpCore.deterministic_coreference(sentence)
        return coreference

    def spacyDependencyParser(self, sentence):
        nlp = spacy.load('en_core_web_md')
        document = nlp(unicode(sentence, "utf-8"))
        return document.print_tree(light=True)



    def spacy_verb_finder(self, sentence):
        nlp = spacy.load('en_core_web_md')
        doc = nlp(sentence.decode('utf-8'))
        for chunk in doc.noun_chunks:
            chunk_root = [chunk.root.text for chunk in doc.noun_chunks]
        print("chunk root:", chunk_root)
        return chunk_root

    def spacy_noun_finder(self, sentence):
        nlp = spacy.load('en_core_web_md')
        doc = nlp(sentence.decode('utf-8'))
        for chunk in doc.noun_chunks:
            chunk_root_head = [chunk.root.head.text for chunk in doc.noun_chunks]
        #print(listChunk)
        print("chunk_root_head: ", chunk_root_head)
        return chunk_root_head



    def textblob_sentiment_analysis(self, sentence):
        blob = TextBlob(sentence, analyzer=NaiveBayesAnalyzer())
        if blob.sentiment.p_pos > blob.sentiment.p_neg:
            return True
        else:
            return False

    def similarity_jaccard(self, first_input, second_input):
        print("text similarity with jaccard")
        similarity_level = similarity.jaccard(first_input, second_input)
        print("similarity_level: ", similarity_level)
        if similarity_level > 0.50:
            return True
        else:
            return False

    def similarity_jaro_winkler(self, first_input, second_input):
        print("text similarity with jaro_winkler")
        similarity_level = similarity.jaro_winkler(str(first_input), str(second_input))
        print("similarity_level: ", similarity_level)
        if similarity_level > 0.50:
            return True
        else:
            return False

    def similarity_levenshtein(self, first_input, second_input):
        print("text similarity with levenshtein")
        similarity_level = similarity.levenshtein(str(first_input), str(second_input))
        print("similarity_level: ", similarity_level)
        if similarity_level >= 0.53:
            return True
        else:
            return False

    def similarity_word_levensthein(self, first_input, second_input):
        print("text similarity with levenshtein")
        similarity_level = similarity.levenshtein(str(first_input), str(second_input))
        print("similarity_level: ", similarity_level)
        if similarity_level > 0.50:
            return True
        else:
            return False


    def spacyDetailedDependencyChunk(self, sentence):
        nlp = spacy.load('en_core_web_md')
        doc = nlp(sentence.decode('utf-8'))
        chunk_text = [chunk.text for chunk in doc.noun_chunks]
        chunk_root = [chunk.root.text for chunk in doc.noun_chunks]
        chunk_root_dep = [chunk.root.dep_ for chunk in doc.noun_chunks]
        chunk_root_head = [chunk.root.head.text for chunk in doc.noun_chunks]
        print("ChunkText: ", chunk_text)
        print("ChunkRoot: ", chunk_root)
        print("ChunkRootHead: ", chunk_root_head)
        print("Chunk root dep: ", chunk_root_dep)
        return chunk_root_dep

    def spacyDependencyRelations(self, sentence):
        nlp = spacy.load('en_core_web_md')
        doc = nlp(sentence.decode('utf-8'))
        token_text = [token.text for token in doc]
        token_dep = [token.dep_ for token in doc]
        token_head_text = [token.head.text for token in doc]
        token_head_pos = [token.pos_ for token in doc]
        token_child = ([child for child in token.children] for token in doc)
        # dataframe = pd.DataFrame(zip(token_text, token_dep, token_head_text, token_head_pos, token_child),
        #                          columns = ['Token Text', 'Token Dep', 'Token Head Text', 'Token Head Pos', 'Token Child'])
        # dataframe.to_html('Dependencies.html')
        print("token_text: ", token_text)
        print("token dep: ", token_dep)
        print("token_head_text: ", token_head_text)
        print("token head pos: ", token_head_pos)
        print("token child: ", token_child)
        #print(dataframe)
        return token_head_pos ,token_text

    def spacyArchMatching(self, sentence):
        verbs = []
        nlp = spacy.load("en_core_web_md")
        doc = nlp(sentence.decode('utf-8'))


        for possible_verb in doc:
            if possible_verb.pos == VERB:
                for possible_subject in possible_verb.children:
                    if possible_subject.dep == nsubj or possible_subject.dep == dobj or possible_subject.dep == ccomp or possible_subject.dep == root:
                        verbs.append(possible_verb)
                        break

        print('VERBS', verbs)
        return verbs

    def spacyDependencyChunk(self, sentence):
        listChunk = []
        indirectDependency = False
        #A medium English model based on spacy -- Size 161 Mo -- Recommended
        nlp = spacy.load('en_core_web_md')
        doc = nlp(sentence.decode('utf-8'))
        # for chunk in doc.noun_chunks:
        #     chunk_root_dep = [chunk.root.dep_ for chunk in doc.noun_chunks]
        #     chunk_root = [chunk.root.text for chunk in doc.noun_chunks]
        #     chunk_root_head = [chunk.root.head.text for chunk in doc.noun_chunks]
        #     chunk_text = [chunk.text for chunk in doc.noun_chunks]
        # print("chunk root dep: ", chunk_root_dep)
        # print("chunk root:", chunk_root)
        # print("chunk_root_head: ", chunk_root_head)
        # print("chunk_text:", chunk_text)
        # print(" ")

        for chunk in doc.noun_chunks:
            #u'dobj' or u'advmod'
            chunk_root_dep = [chunk.root.dep_ for chunk in doc.noun_chunks]
            # if (u'dobj' and u'nsubj') or u'advmod' in str(chunk.root.dep_):
            #     indirectDependency = True
            # elif u'nsubj' in str(chunk.root.dep_):
            #     indirectDependency = False

        print("chunk root dep: ", chunk_root_dep)
        if chunk_root_dep[-1] == u'nsubj' and len(chunk_root_dep) == 1:
            indirectDependency = False
        elif len(chunk_root_dep) > 1:
            if chunk_root_dep[-2] == u'nsubj' and chunk_root_dep[-1] == u'dobj':
                indirectDependency = True
            elif chunk_root_dep[-2] == u'dobj' and chunk_root_dep[-1] == u'nsubj':
                indirectDependency = False

        print("indirectDependency: ", indirectDependency)

        return indirectDependency

    #Install en_coref_md
    #pip install en_coref_sm-3.0.0.tar.gz
    def spacyCoreferenceResolution(self, sentence):
        #nlp = spacy.load('en_coref_md')
        nlp = en_coref_lg.load()
        doc = nlp(unicode(sentence, encoding="utf-8"))
        #doc = unicode_(sentence)
        if doc._.has_coref is True:
            print(doc._.coref_clusters)
            mentions = [{'start': mention.start_char,
                         'end': mention.end_char,
                         'text': mention.text,
                         'resolved': cluster.main.text
                         }
                        for cluster in doc._.coref_clusters
                        for mention in cluster.mentions]
            clusters = list(list(span.text for span in cluster)
                            for cluster in doc._.coref_clusters)
            resolved = doc._.coref_resolved

        return doc._.has_coref

    def textblobPatternParser(self, sentence):
        blob = TextBlob(sentence, parser=PatternParser())
        return blob.parse()

    # def spell_checker_input(self, statement):
    #     print("statement is: ", statement)
    #     result = enchant.Dict("en-US") ##Spell Checking tokenize words
    #     print(list(set([word.encode('ascii', 'ignore') for word in word_tokenize(result) if result.check(word) is False and re.match('^[a-zA-Z ]*$',word)])))

    def stanfordCoreferenceResolution(self, statement):
        nlp = StanfordCoreNLP(r'G:\AllFiles\Projeler\OpenSource\SemanticWeb&NLP\stanford-corenlp-full-2018-02-27\stanford-corenlp-full-2018-02-27', quiet=False)
        props = {'annotators': 'coref', 'pipelineLanguage': 'en'}
        result = json.loads(nlp.annotate(statement, properties = props))
        num, mentions = result['corefs'].items()[0]
        for mention in mentions:
            print(mention)


    def namedEntityRecognition(self, param_ner):
        try:
            nerResult = nlpCore.ner(param_ner)
            print(nerResult)
        except Exception as ex:
            logger.exception("Named Entity Recognition Error ")

    def spacy_verb_lemmatizer(self, param_to_be_lemmatized):
        lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
        lemmas = lemmatizer(param_to_be_lemmatized, u'VERB')
        return lemmas

    def spacy_noun_lemmatizer(self, noun_to_be_lemmatized):
        lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
        lemmas = lemmatizer(noun_to_be_lemmatized, u'NOUN')
        return lemmas

    def posTaggerSender(self, param_posTagger):
        try:
            posResult = nlpCore.posTagger(param_posTagger)
        except Exception as ex:
            logger.exception("Pos Tagger Error")
        return posResult

    #Tested with Server. Stanford CoreNLP server up and running
    def constituencyParser(self, param_constituent):
        try:
            constituentParseTree = nlpCore.parse(param_constituent)
            # print(constituentParseTree)
            return Tree.fromstring(constituentParseTree)
        except Exception as ex:
            logger.exception("Constituency Parser error")

    def resultSentiment(self, param_sentiment):
        try:
            sentiment_analysis = nlpCore.annotate(param_sentiment)
            print(sentiment_analysis)
        except Exception as ex:
            logger.exception("Sentiment Analysis error")

    #Find tree's node with the following method
    #get_node function has been changed with label() function
    def printSubtrees(self, tree, constituentTags, extraCheckTags=None):
        try:
            for subtree in tree.subtrees():
                if subtree.label() == constituentTags or subtree.label() == extraCheckTags:
                    return subtree.leaves()
        except Exception as e:
            logger.exception("Subtree parse problem")

    def findNNSubtree(self, tree):
        try:
            NPs = list(tree.subtrees(filter=lambda x: x.label() == 'NP'))
            NNs_insideNPs = map(lambda x: list(x.subtrees(filter=lambda x: x.label() == 'NNP' or x.label() == 'NN' or  x.label() == 'NNS')), NPs)
            return self.removeDuplicates([noun.leaves()[0] for nouns in NNs_insideNPs for noun in nouns])
        except Exception as ex:
            logger.exception("Constituency Parser error")

    def findVPSubtree(self, tree):
        try:
            VPs = list(tree.subtrees(filter=lambda x: x.label() == 'VP' or x.label() == 'VBZ'
                                     or x.label() == 'VBD' or x.label() == 'VBG' or x.label() == 'VBN' or x.label() == 'VBP'))
            print("length of VPs", len(VPs))
            print("VPs", VPs)
            if len(VPs) == 0:
                return None
            #or x.label() == 'VB'
            VBZs = map(lambda x: list(x.subtrees(filter=lambda x: x.label() == 'VBZ')), VPs)
            print("VBZ", VBZs)
            return self.removeDuplicates([verb.leaves()[0] for verbs in VBZs for verb in verbs])
        except Exception as ex:
            logger.exception("VPSubtree Parser Error")



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
    def wordnetLatentAnalysis(self, word1, word2, lch_threshold=2.15, verbose=False):
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

