import nltk
import re
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import SparqlQueryParser


def nltkWordFreq(tokens):
    freq_dist_nltk = nltk.FreqDist(tokens)
    print(freq_dist_nltk)
    for k,v in freq_dist_nltk.items():
        print (str(k) + str(v))
    return freq_dist_nltk

def sentenceTokenize(textInput):
    resultSentence = sent_tokenize(textInput)
    return resultSentence


#Stopwords need to be cleared out
def clearTokenAndStopWords(tokensParam):
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

def pureWordfreq (tokens):
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



def parsingFunc():
    sentence = "I was getting through this"
    tokens = nltk.word_tokenize(sentence)
    wordnetWords = wordnet.synsets("spectacular")
    print(wordnetWords)
    print(wordnetWords[0].definition())

    print(tokens)

#tagged sentence in case of who
def taggedWhoQuestion(tagged_words):
    if(tagged_words[0][1] == 'WP'):
        name = ''
        counter = 0
        for word in tagged_words:
            if(word[1] == 'NNP'):
                if(counter == 0 ):
                    name += word[0]
                else:
                    name += ' ' + word[0]

                counter +=1
        SparqlQueryParser.WhoIsFunc(name)

#tagged sentence in case of where
def taggedWhereQuestion(tagged_words):
    if(tagged_words[0][1] == 'WRB'):
        place = ''
        counter = 0
        for word in tagged_words:
            if(word[1] != 'WRB' and word[1] != '.'):
                if(counter == 0):
                    place += word[0]
                else:
                    place += ' ' + word[0]

                counter += 1
        SparqlQueryParser.whereIsFunc(place)

def taggedWhatQuestion(tagged_words):#
    if(tagged_words[0][1] == 'WP' and tagged_words[0][0] == 'What'):
        item = ''
        counter = 0
        for word in tagged_words:
            if(word[1] != 'WP' and word[1] != '.'):
                if(counter == 0):
                    item += word[0]
                else:
                    item += ' ' + word[0]

                counter += 1
        SparqlQueryParser.whatIsFunc(item)

