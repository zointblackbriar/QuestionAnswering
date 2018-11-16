import StanfordCoreNLP
import json, ast


class TestStanfordCoreNLP():

    def __init__(self):
        corenlpObject = StanfordCoreNLP.TestConnectionCoreNLP()

    """test for questions"""
    def sentenceDependencyParseTest(self, sentence):
        tree = self.corenlpObject.constituencyParser(sentence)
        print(self.corenlpObject.findVPSubtree(tree))
        value = ast.literal_eval(json.dumps(self.corenlpObject.findVPSubtree(tree)[0]))
        print(self.corenlpObject.wordnetLatentAnalysis(value, "contains"))


obj = TestStanfordCoreNLP()
obj.sentenceDependencyParseTest("What contains iwu?")



# obj.namedEntityRecognition("What is the value of sensor1 in machine1 between 11/6/2018-16.58 and 11/6/2018-17.59")
# obj.dependencyParser("What linkedfactory contains?")

# if obj.dependencyParser("What incorporates rollex?") == [(u'ROOT', 0, 2), (u'nsubj', 2, 1), (u'dobj', 2, 3), (u'punct', 2, 4)]:
#     print("First")
# elif obj.dependencyParser("What linkedfactory contains?") == [(u'ROOT', 0, 3), (u'det', 2, 1), (u'nsubj', 3, 2), (u'punct', 3, 4)]:
#     print("Second")
# else:
#     print("Unavaliable")

# print(obj.posTaggerSender("What contains ha100?"))
# print(type(obj.posTaggerSender("What contains ha100?")))
# matching = [s for s in obj.posTaggerSender("What contains ha100?") if 'VBZ' in s]
# print(matching)
# if [(u'contains', u'VBZ')] == [s for s in obj.posTaggerSender("What contains ha100?") if 'VBZ' in s]:
#     print("true result")
# else:
#     print("no result")
# tree = obj.constituencyParser("What contains ha100?")
# print(obj.findVPSubtree(tree))
# value = ast.literal_eval(json.dumps(obj.findVPSubtree(tree)[0]))
# print(obj.wordnetLatentAnalysis(value, "contains"))

