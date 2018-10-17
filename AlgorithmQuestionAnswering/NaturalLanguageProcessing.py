import nltk
from nltk.corpus import stopwords
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class NaturalProcess:
    def wordFrequencyCount(self, token):
        """nltk default stopwords"""
        #standart lowercase
        words = self.removeStopWords(token)
        words = [word.lower() for word in words]
        logger.info("lowercase occurred {}")

        #calculate frequency of words
        fdist = nltk.FreqDist(words)
        print("fdist", fdist)
        return fdist

    def removeStopWords(self, param_input):
        defaultEnglishStopwords = set(nltk.corpus.stopwords.words('english'))
        """if you want to add some custom stopwords you can use the following code snippet"""
        #stopwords_file = './stopwords.txt'
        #custom_stopwords = set(codes.open(stopwords_file, 'r', 'utf-8').read().splitlines())
        #all_stopwords = defaultEnglishStopwords | custom_stopwords
        words = nltk.word_tokenize(param_input)
        logger.info("nltk word tokenize")
        #Remove single-character tokens (mostly punctuation
        words = [word for word in words if len(word) > 1]
        logger.info("nltk remove single characters")
        #Remove numbers
        words = [word for word in words if word.isnumeric()]
        logger.info("nltk remove numbers")

        #Remove stopwords
        new_tokens = [w for w in words if not w in defaultEnglishStopwords]
        return new_tokens

def takeASentenceInput():
    sentence = input("Enter your sentence")

#assert testSentenceTokenizer() == "true input"
