import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import CFG, PCFG
from nltk.parse.generate import generate, demo_grammar


class NLTKProp(object):
    def nltkWordFreq(self, tokens):
        freq_dist_nltk = nltk.FreqDist(tokens)
        print(freq_dist_nltk)
        for k,v in freq_dist_nltk.items():
            print (str(k) + str(v))
        return freq_dist_nltk

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



    def parsingFunc(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        wordnetWords = wordnet.synsets("spectacular")
        # print(wordnetWords)
        # print(wordnetWords[0].definition())
        # print(tokens)
        return wordnetWords

    def CFGParser(self, tree):
        grammar = CFG.fromstring(tree)
        grammar.start()
        grammar.productions()

    def probabilisticCFG(self, tree):
        grammar = PCFG.fromstring(tree)
        grammar.start()
        grammar.productions()

    def contextFreeGrammar(self, sentence):
        sent = sentence.split()
        parser = nltk.ChartParser(gr)

grammarTest = NLTKProp().CFGParser(demo_grammar)
print(grammarTest)


sentence = "I was getting through this"
print(NLTKProp().parsingFunc(sentence))