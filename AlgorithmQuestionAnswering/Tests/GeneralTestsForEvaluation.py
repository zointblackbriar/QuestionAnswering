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

    def test_union_query_of_a_sentence_q_1(self):
        comparison = []
        statement = "What do linkedfactory, heatmeter, and e3fabrik incorporate exactly?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    # def test_question_union_second(self):
    #     comparison = []
    #     statement = "What do linkedfactory, iwu  contain?"
    #     query_linked_factory = Utils.questionMarkProcess(statement)
    #     sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_linked_factory)
    #     for row in sparqlQuery:
    #         comparison.append(row)
    #     self.assertFalse(isinstance(comparison[0], str))

    def test_question_union_third_q_2(self):
        comparison = []
        statement = "Provide me a combined result for IWU and e3sim"
        query_linked_factory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_linked_factory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))



    def test_affirmative_member_question_q_3(self):
        comparison = []
        statement = "I want to know which one carries fofab?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_affirmative_member_question_second_version_q_4(self):
        comparison = []
        statement = "There is a member named fofab. Please give me all of its members?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_dynamic_indirect_question_third_version_q_5(self):
        comparison = []
        statement = "I am a customer for this company. Could you tell me please what  the value of sensor1 of machine1 is?"
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


    def test_wordnet_similarity_version_first_q_6(self):
        comparison = []
        statement = "What linkedfactory holds?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_wordnet_similarity_version_third_q_7(self):
        comparison = []
        statement = "What does linkedfactory holds?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_wordnet_similarity_version_second_q_8(self):
        comparison = []
        statement = "What does machine1 incorporate?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_adjective_data_q_9(self):
        comparison = []
        statement = "What does gmx comprise?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_inverse_query_q_10(self):
        comparison = []
        statement = "What comprises karobau?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_dynamic_system_health_question_version_first_q_11(self):
        comparison = []
        statement = "system health for sensor2 in machine6"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_dynamic_system_health_question_version_second_q_12(self):
        comparison = []
        statement = "Tell me the health of system for sensor2 in machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #bu soruyu degistir
    def test_dynamic_system_health_question_version_third_q_13(self):
        comparison = []
        statement = "system health for sensor1 in machine2"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_opc_generated_query_q_14(self):
        comparison = []
        statement = "Could you browse generated data?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_affirmative_static_question_q_15(self):
        comparison = []
        statement = "Give me the all of members in linkedfactory?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_indirect_question_q_16(self):
        comparison = []
        statement = "What holds linkedfactory?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        resultOfConstituentParse = corenlpObject.constituencyParser(queryLinkedFactory)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_static_question_q_17(self):
        comparison = []
        statement = "What is the hiearchical structure of fofab?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        resultOfConstituentParse = corenlpObject.constituencyParser(queryLinkedFactory)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_second_indirect_question_q_18(self):
        statement = "What contains IWU?"
        comparison = []
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_direct_question_q_19(self):
        statement = "Could you give me the members in which contained by linkedfactory?"
        comparison = []
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    #@unittest.skip("Last query will be tested")
    def test_what_indirect_question_expanded_q_20(self):
        statement = "Could you give me the members in which linkedfactory has?"
        comparison = []
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
        testList = []
        for row in sparqlQuery["results"]["bindings"]:
            testList.append(row)
        self.assertEqual(isinstance(testList[0], str))


    #@unittest.skip("Last query will be tested")
    def test_dynamic_question_q_21(self):
        statement = "What is the value of sensor1 in machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertNotEqual(sparqlQuery.get('value'), '6.33333')

    #@unittest.skip("Last query will be tested")
    def test_dynamic_minimum_question_q_22(self):
        statement = "What is the minimum that we can calculate for sensor1 in machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertNotEqual(sparqlQuery.get('min'), '6.33333')

    #@unittest.skip("Last query will be tested")
    def test_dynamic_maximum_question_q_23(self):
        statement = "What is the maximum that one can calculate for sensor1 of machine1?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertNotEqual(sparqlQuery.get('max'), '6.33333')

    #@unittest.skip("Last query will be tested")
    def test_dynamic_average_question_type_one_q_24(self):
        statement = "Could you tell me what the average for sensor3 in machine3 is?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertEqual(sparqlQuery.get('avg'), '6.33333')

    def test_dynamic_average_indicative_question_q_25(self):
        statement = "I need to learn an average for sensor5 in machine2"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertEqual(sparqlQuery.get('avg'), '6.33333')


    #@unittest.skip("Last query will be tested")
    def test_dynamic_average_question_type_two_q_26(self):
        statement = "What is the average of sensor3 in machine3?"
        queryLinkedFactory = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
        self.assertNotEqual(sparqlQuery.get('avg'), '6.33333')

    def test_opc_generated_references_of_nodes_q_27(self):
        comparison = []
        statement = "Could you get me the references of nodes?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_browse_query_q_28(self):
        comparison = []
        statement = "Could you browse generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_wordnet_browse_query_q_29(self):
        comparison = []
        statement = "Could you range within generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_take_query_q_30(self):
        comparison = []
        statement = "Could you take me all members of  generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_opc_generated_nodeid_q_31(self):
        comparison = []
        statement = "Give me all registered node id?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    #@unittest.skip("nodeid query will be tested")

    def test_opc_generated_parent_node_id_q_32(self):
        comparison = []
        statement = "I need to learn parent node id in generated data"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))


    def test_opc_generated_parent_node_id_second_version_q_33(self):
        comparison = []
        statement = "Could you give me parent node id in the file of generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))


    #@unittest.skip("nodeid query will be tested")

    def test_opc_generated_query_data_block_q_34(self):
        comparison = []
        statement = "Give me all data blocks"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    #Can you browse OPC UA Generated Data?
    def test_opc_generated_data_alternative_way_q_35(self):
        comparison = []
        statement = "Can you browse OPC UA Generated Data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_query_data_block_q_36(self):
        comparison = []
        statement = "Give me all data blocks"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_query_data_block_second_version_q_37(self):
        comparison = []
        statement = "data blocks in generated OPC file"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_query_station_identify_q_38(self):
        comparison = []
        statement = "Give me the name of stations in generated data"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_opc_generated_query_station_identify_second_version_q_39(self):
        comparison = []
        statement = "All stations which are in generated data or new data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_1_q_40(self):
        comparison = []
        statement = "please give me combined result of datablock, station"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_2_q_41(self):
        comparison = []
        statement = "Give me all members of BHKW"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_3_q_42(self):
        comparison = []
        statement = "Who is fofab?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_4_q_43(self):
        comparison = []
        statement = "There is a member named fofab. Please give me all of its members"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_5_q_44(self):
        comparison = []
        statement = "Could you provide me please what is the value of sensor3 in machine7"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_6_q_45(self):
        comparison = []
        statement = "I need to learn an average value for sensor1 in machine8"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_factoid_1_q_46(self):
        comparison = []
        statement = "What is the number of members in BHKW?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_inductive_q_47(self):
        comparison = []
        statement = "Why should I browse in generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_reasoning_q_48(self):
        comparison = []
        statement = "Can you tell me the system in trouble for sensor1 in machine3?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.dynamic_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_reasoning_q_49(self):
        comparison = []
        statement = "Is the E3-Sim member of linkedfactory?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.static_query_triples(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))

    def test_question_reasoning_q_50(self):
        comparison = []
        statement = "List all references of generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertTrue(isinstance(comparison[0], str))


if __name__ == '__main__':
    unittest.main()
