import os
os.chdir(r'../')

import unittest
import StanfordSpacyNLP
import Utils
from SPARQLGenerator import SPARQLGeneratorClass

corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()

class BaseTestCase(unittest.TestCase):
    def test_factoid_question_first(self):
        comparison = []
        statement = "What are the members of aximus exactly?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_factoid_question_second(self):
        comparison = []
        statement = "What do linkedfactory, iwu  contain?"
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_factoid_question_third(self):
        comparison = []
        statement = "What does linkedfactory contain?"
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_factoid_question_fourth(self):
        comparison = []
        statement = "What is fofab?"
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_factoid_question_fifth(self):
        comparison = []
        statement = "What does fofab hold inside?"
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_keyword_question_first(self):
        comparison = []
        statement = "contains fofab"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_keyword_question_second(self):
        comparison = []
        statement = "average of sensor1 in machine1 "
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_keyword_question_third(self):
        comparison = []
        statement = "value of sensor7 in machine3"
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_keyword_question_fourth(self):
        comparison = []
        statement = "minimum of sensor1 in machine7"
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_keyword_question_fifth(self):
        comparison = []
        statement = "health status sensor1 machine1"
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))





if __name__ == '__main__':
    unittest.main()
