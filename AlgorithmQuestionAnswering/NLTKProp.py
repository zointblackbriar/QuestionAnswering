#!/usr/bin/env python
# coding: utf-8


import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import CFG, PCFG
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import requests
import ast


class NLTKProp():
    #Calculate word frequency with NLTK
    def nltkWordFreq(self, tokens):
        freq_dist_nltk = nltk.FreqDist(tokens)
        print(freq_dist_nltk)
        for k,v in freq_dist_nltk.items():
            print (str(k) + str(v))
        return freq_dist_nltk

    #Sentence tokenization
    def sentenceTokenize(self, textInput):
        resultSentence = sent_tokenize(textInput)
        return resultSentence


    #Stopwords need to be cleared out
    def clearTokenAndStopWords(self, tokensParam):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(tokensParam)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []

        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        # print(word_tokens)
        # print(filtered_sentence)
        return filtered_sentence

    #Could be duplicated with nltkWordFreq
    def pureWordfreq (self, tokens):
        '''
        Function to generated the frequency distribution of the given text
        :param tokens:
        :return:
        '''
        word_freq = {}
        for tok in tokens.split():
            if tok in word_freq:
                word_freq[tok] += 1
            else:
                word_freq[tok] = 1

        print("Word freq: ", word_freq)
        return word_freq

    #Word Tokenization
    def wordTokenize(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        wordnetWords = wordnet.synsets("spectacular")
        return wordnetWords

    def CFGParser(self, tree):
        grammar = CFG.fromstring(tree)
        grammar.start()
        grammar.productions()

    def probabilisticCFG(self, tree):
        grammar = PCFG.fromstring(tree)
        grammar.start()
        grammar.productions()

    #NaiveBayesClassifier
    #This function should be optimized
    def trainSentimentAnalysis(self, sentence):
        # Install all instances of subjectivity
        n_instances = 100
        subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
        obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
        print(len(subj_docs), len(obj_docs))
        print(subj_docs[1])
        train_subj_docs = subj_docs[:80]
        test_subj_docs = subj_docs[80:100]
        train_obj_docs = obj_docs[:140]
        test_obj_docs = obj_docs[80:1000]
        training_docs = train_subj_docs + train_obj_docs
        testing_docs = test_subj_docs+test_obj_docs
        sentimental_analyzer = SentimentAnalyzer()
        all_words_negative = sentimental_analyzer.all_words([mark_negation(doc) for doc in training_docs])
        unigram_feats = sentimental_analyzer.unigram_word_feats(all_words_negative, min_freq=4)
        print(len(unigram_feats))
        sentimental_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
        training_set = sentimental_analyzer.apply_features(training_docs)
        test_set = sentimental_analyzer.apply_features(testing_docs)
        trainer = NaiveBayesClassifier.train
        classifier = sentimental_analyzer.train(trainer, training_set)
        #Training classifier
        for key, value in sorted(sentimental_analyzer.evaluate(test_set).items()):
            print('{0}: {1}'.format(key, value))

        sid = SentimentIntensityAnalyzer()
        print(sentence)
        ss = sid.polarity_scores(sentence)
        print(ss)
        # for k in sorted(ss):
        #     print('{0}: {1}, '.format(k, ss[k]))
        # print()

    def externalSentimentAnalysis(self, sentence):
        headers = {'Content-Type': 'application/json'}
        print(sentence)
        data = "text=" + str(sentence)
        print(data)
        response = requests.post('http://text-processing.com/api/sentiment/', data=data,
                                 headers=headers)
        print(response)

        if response.status_code == 200:
            print ('Status code 200')
            #sentimentResult = json.loads(response.content.decode('utf-8'))
            #sentimentResult = json.dumps(sentimentResult)
            sentimentResult = response.content.decode('utf-8')
            data = ast.literal_eval(sentimentResult)
            print(type(data))
            if data['label'] == 'neg':
                return False
        else:
            print('Status code something else')
            return None
        return True

    @staticmethod
    def stemmingPorter(item):
        porter_stemmer = PorterStemmer()
        return porter_stemmer.stem(item)

    @staticmethod
    def stemmingSnowball(item):
        item = str(item).lower()
        snowball_stemmer = SnowballStemmer("english")
        return snowball_stemmer.stem(item)

    @staticmethod
    def lemmatization(item):
        wordnet_lemmatizer = WordNetLemmatizer()
        print(wordnet_lemmatizer.lemmatize(item))

