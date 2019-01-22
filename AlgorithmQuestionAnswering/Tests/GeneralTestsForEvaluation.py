#!/usr/bin/env python
# coding: utf-8
import os
os.chdir(r'../')

import unittest
import StanfordSpacyNLP
import Utils
from SPARQLGenerator import SPARQLGeneratorClass

corenlpObject = StanfordSpacyNLP.TestConnectionCoreNLP()

class BaseTestCase(unittest.TestCase):

    # query = "What linkedfactory and heatmeter and e3fabrik incorporate"
    # queryTest = "What linkedfactory holds"
    # querySeconds = "Give me all members of BHKW"
    # queryThird = "Give me all the machines in demofactory?"

    def test_union_query_of_a_sentence(self):
        comparison = []
        statement = "What do linkedfactory and heatmeter and e3fabrik incorporate?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_question_union_second(self):
        comparison = []
        statement = "What do linkedfactory, iwu  contain?"
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))


    def test_affirmative_member_question(self):
        comparison = []
        statement = "I want to know which one contains fofab?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_affirmative_member_question_second_version(self):
        comparison = []
        statement = "There is a member named fofab. Please give me all of its members?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_dynamic_indirect_question_third_version(self):
        comparison = []
        statement = "I am a customer for this company. Could you tell me please what is the value of sensor1 in machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_dynamic_indirect_question_fourth_version(self):
        comparison = []
        statement = "Could you tell me please what is the current value of sensor2 in machine2?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))


    def test_wordnet_similarity_version_first(self):
        comparison = []
        statement = "What linkedfactory holds?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_wordnet_similarity_version_third(self):
        comparison = []
        statement = "What linkedfactory incorporates?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_wordnet_similarity_version_second(self):
        comparison = []
        statement = "What does fofab incorporate?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_adjective_data(self):
        comparison = []
        statement = "What does fofab contain?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_inverse_query(self):
        comparison = []
        statement = "What contains fofab?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_dynamic_system_health_question_version_first(self):
        comparison = []
        statement = "system health for sensor2 in machine6?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_dynamic_system_health_question_version_second(self):
        comparison = []
        statement = "Could you tell me the system health for sensor2 in machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_dynamic_system_health_question_version_third(self):
        comparison = []
        statement = "health for sensor1 in machine2? "
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_opc_generated_query(self):
        comparison = []
        statement = "Could you browse generated data?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_affirmative_static_question(self):
        comparison = []
        statement = "Give me the all of members of linkedfactory?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_indirect_question(self):
        comparison = []
        statement = "What contains linkedfactory?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        resultOfConstituentParse = corenlpObject.constituencyParser(queryLinkedFactory)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_static_question(self):
        comparison = []
        statement = "What does fofab contain?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        resultOfConstituentParse = corenlpObject.constituencyParser(queryLinkedFactory)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_second_indirect_question(self):
        statement = "What contains IWU?"
        comparison = []
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_direct_question(self):
        statement = "Could you give me the members in which contained by linkedfactory?"
        comparison = []
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_indirect_question_expanded(self):
        statement = "Could you give me the members in which one contains linkedfactory?"
        comparison = []
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        testList = []
        for row in sparqlQuery["results"]["bindings"]:
            testList.append(row)
        self.assertEqual(isinstance(testList[0], str))


    #@unittest.skip("Last query will be tested")
    def test_dynamic_question(self):
        statement = "What is the value of sensor1 in machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertNotEqual(sparqlQuery.get('value'), '6.33333')

    #@unittest.skip("Last query will be tested")
    def test_dynamic_minimum_question(self):
        statement = "What is minimum for sensor1 in machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertNotEqual(sparqlQuery.get('min'), '6.33333')

    #@unittest.skip("Last query will be tested")
    def test_dynamic_maximum_question(self):
        statement = "What is maximum for sensor1 in machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertNotEqual(sparqlQuery.get('max'), '6.33333')

    #@unittest.skip("Last query will be tested")
    def test_dynamic_average_question_type_one(self):
        statement = "Could you tell me what is average for sensor3 in machine3?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertEqual(sparqlQuery.get('avg'), '6.33333')

    def test_dynamic_average_indicative_question(self):
        statement = "I need to learn an average for sensor5 in machine2?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertEqual(sparqlQuery.get('avg'), '6.33333')


    #@unittest.skip("Last query will be tested")
    def test_dynamic_average_question_type_two(self):
        statement = "What is the average of sensor3 in machine3?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertNotEqual(sparqlQuery.get('avg'), '6.33333')

    def test_opc_generated_references_of_nodes(self):
        comparison = []
        statement = "Could you get me the references of nodes?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_browse_query(self):
        comparison = []
        statement = "Could you browse generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_wordnet_browse_query(self):
        comparison = []
        statement = "Could you graze generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))


    def test_opc_generated_take_query(self):
        comparison = []
        statement = "Could you take me generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_opc_generated_nodeid(self):
        comparison = []
        statement = "Give me all registered node id?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    #@unittest.skip("nodeid query will be tested")

    def test_opc_generated_parent_node_id(self):
        comparison = []
        statement = "I need to learn parent node id in generated data"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))


    def test_opc_generated_parent_node_id_second_version(self):
        comparison = []
        statement = "Could you give me parent node id in the file of generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))


    #@unittest.skip("nodeid query will be tested")

    def test_opc_generated_query_data_block(self):
        comparison = []
        statement = "Give me all data blocks?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_query_data_block_second_version(self):
        comparison = []
        statement = "data blocks in generated OPC file?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_query_station_identify(self):
        comparison = []
        statement = "Give me the name of Stations in generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_query_station_identify_second_version(self):
        comparison = []
        statement = "All station which is in generated data or new data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_1(self):
        comparison = []
        statement = "What fofab contains?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_2(self):
        comparison = []
        statement = "Give me all members of linkedfactory"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_3(self):
        comparison = []
        statement = "I want to know which one contain fofab"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_4(self):
        comparison = []
        statement = "There is a member named fofab. Please give me all of its members"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_5(self):
        comparison = []
        statement = "Could you tell me please what is the value of sensor3 in machine7"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_6(self):
        comparison = []
        statement = "I need to learn an average for sensor1 in machine8"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))







if __name__ == '__main__':
    unittest.main()
