#!/usr/bin/env python
# coding: utf-8

import unittest
import os
os.chdir(r'../')
import Utils
from SPARQLGenerator import SPARQLGeneratorClass
from time import time


class BaseTestClass(unittest.TestCase):


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
        start_time = time()
        comparison = []
        statement = "Could you take me generated data?"
        query_generated_data = Utils.questionMarkProcess(statement)
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data)
        for row in sparqlQuery:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))
        end_time=time()
        print("total amount of time is required: ", end_time - start_time)

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
        sparqlQuery = SPARQLGeneratorClass.generated_data_query_OPC(query_generated_data, 2)
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




if __name__ == '__main__':
    unittest.main()

