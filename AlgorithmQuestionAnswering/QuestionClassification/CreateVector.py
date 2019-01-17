#Reference https://github.com/swapkh91/Question-Classification

import numpy as np
import random
import operator
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim

import logging
import pdb

logging.info('Started logger for...')
logger = logging.getLogger(__name__)
#os.chdir(r'../')


word_vector_path = "glove/glove.6B.50d.txt"
vector_dim = 50
word_vector = gensim.models.KeyedVectors.load_word2vec_format(word_vector_path, binary=False)


class WordVector():
    @staticmethod
    def create_vector(question):
        global word_vector
        splitted = question.split(" ")
        #splitted = question
        #make zeros into all values of vector
        vector = np.zeros(vector_dim)
        count = 2.0
        try:
            if len(splitted) == 0:
                return vector
            else:
                vector = map(operator.add, word_vector[splitted[0].lower()], vector)
                if len(splitted) == 1:
                    return np.asarray(vector)
                vector = map(operator.add, word_vector[splitted[1].lower()], vector)
                if(splitted[0].lower() == 'what' and splitted[1].lower() == 'is'):
                    count = 0.0
                    vector = np.zeros(vector_dim)
                    for token in splitted:
                        count += 1
                        try:
                            vector = map(operator.add, word_vector[token.lower()], vector)
                        except KeyError:
                            count -= 1
                    if count == 0:
                        return np.asarray(vector)
                    return np.asarray(vector) / count
                return np.asarray(vector) / count
        except KeyError:
            logger.exception("Word Vector error")
        return vector
