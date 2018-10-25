#!/usr/bin/env python3

from StanfordCoreNLP import TestConnectionCoreNLP
import unicodedata
import Utils

nlpTask = TestConnectionCoreNLP()
#obj.runTest("What contains HeatMeter?")
query = "What linkedfactory and heatmeter and e3fabrik incorporate"
queryTest = "What linkedfactory holds"
querySeconds = "Give me all members of BHKW"
queryThird = "Give me all the machine in demofactory?"
query = Utils.questionMarkProcess(query)
#tree = nlpTask.runTest(query)
#treeV2 = nlpTask.runTest(querySeconds)
treev3 = nlpTask.runTest(queryThird)
print(treev3.pretty_print(unicodelines=False, nodedist=4))
print(treev3.leaves())

nounTag = nlpTask.printSubtrees(treev3, 'NP', 'NN')
import json, ast
result = ast.literal_eval(json.dumps(nounTag))
print("result", result)
#print(nlpTask.simulation('contains', result[0]))

# obj.synonym("contain")

#test synonym process
#obj.synonymProcess("What contains heatmeter", "incorporate")
#test synonym process
#obj.synonymProcess("Hello World incorporate", "incorporate")

#print(nlpTask.simulation('contains', result[0]))