from Utils import *

def testSentenceTokenizer():
    input = "Hello this is the first sentence. This is the second sentence. This is the third sentence."
    result = sentenceTokenize(input)
    print("result of sentence tokenizer: ", result)
    if len(result) > 1:
        return "false input"
    else:
        return "true input"

assert testSentenceTokenizer() == "true input"