from Utils import *

def testSentenceTokenizer():
    input = "Hello this is the first sentence. This is the second sentence. This is the third sentence."
    result = sentenceTokenize(input)
    print(result)

testSentenceTokenizer()