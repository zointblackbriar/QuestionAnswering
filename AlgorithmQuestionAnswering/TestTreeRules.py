# #!/usr/bin/env python3
# # coding: utf-8
# from __future__ import unicode_literals
#
#
# from StanfordCoreNLP import TestConnectionCoreNLP
# import unicodedata
# import Utils
# import NLTKProp
# import json, ast
# import unittest
#
# query = "What linkedfactory and heatmeter and e3fabrik incorporate"
# queryTest = "What linkedfactory holds"
# querySeconds = "Give me all members of BHKW"
# queryThird = "Give me all the machines in demofactory?"
#
# """                   ROOT
#                     |
#                     SQ
#                _____|__________________________
#               VP                               |
#   ____________|_____                           |
#  |    |             NP                         |
#  |    |        _____|__________                |
#  |    |       |                PP              |
#  |    |       |             ___|_______        |
#  |    NP      NP           |           NP      |
#  |    |    ___|_____       |           |       |
#  VB  PRP PDT  DT   NNS     IN          NN      .
#  |    |   |   |     |      |           |       |
# Give  me all the machines  in     demofactory  ?
# """
#
# queryAverage = "What is average value for sensor1 in machine1?"
# """                           ROOT
#                             |
#                           SBARQ
#   __________________________|________________________________________
#  |                          SQ                                       |
#  |     _____________________|_____                                   |
#  |    |                           NP                                 |
#  |    |                      _____|______________________            |
#  |    |                     |                            PP          |
#  |    |                     |                         ___|_____      |
# WHNP  |                     NP                       |         NP    |
#  |    |    _________________|__________________      |         |     |
#  WP  VBZ  DT    NN    ,     NN    CC    NN    NNS    IN        NN    .
#  |    |   |     |     |     |     |     |      |     |         |     |
# What  is the average  ,  minimum and maximum values for     sensor1  ?
#
# """
#
# queryDynamic = "What is the value of sensor1 in machine1"
#
# queryGiveme = "Give me a minimum for sensor1 in machine1"
#
#
# class MyTest(unittest.TestCase):
#     nlpTask = TestConnectionCoreNLP()
#     def __init__(self):
#         pass
#
#
#     def question(self, questionParam):
#         pass
#
#
#     queryAverage = Utils.questionMarkProcess(queryAverage)
#
#
#     treeConstituent = nlpTask.constituencyParser(queryAverage)
#     test = nlpTask.printSubtrees(treeConstituent, "JJ", "")
#     print("test", test)
#     #print(treeConstituent)
#     #treeConstituent = nlpTask.dependencyParser(queryDynamic)
#     #print(treeConstituent.pretty_print())
#     #print(treeConstituent.leaves())
#     #
#     # treeDependency = nlpTask.dependencyParser(queryThird)
#     # print(treeConstituent.pretty_print())
#     # print(treeConstituent.leaves())
#
#
#
#
#     #printsubtree
#     #nounTag = nlpTask.printSubtrees(treeConstituent, 'NN', '')
#     #result = ast.literal_eval(json.dumps(nounTag))
#     #print("resultsubtree", result)
#
#     resultPypi = nlpTask.findSpecificSubtree(treeConstituent)
#     print(resultPypi)
#
#
#
