#!/usr/bin/env python
# coding: utf-8


from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from rdflib.graph import Graph
from rdflib.plugins import sparql
from rdflib import URIRef, Literal
from rdflib.plugin import register, Serializer, Parser
register('ttl', Parser, 'rdflib.plugins.parsers.notation3', 'TurtleParser')
import logging
import colored_logs
import time
from rdflib.plugins.sparql import prepareQuery

logging.info('Starting logger for ...') #or call logging.basicConfig
# Set log name
logger = logging.getLogger(__name__)


class SPARQLEndpoint():

    def __init__(self, endpoint, setQuery, paramFormat, filename=None):
        self._endpoint = endpoint
        self._setQuery = setQuery
        self._paramFormat = paramFormat
        self._filename = filename
        self._sparql = SPARQLWrapper(self._endpoint)

    def SparqlInit(self):
        logger.info("SparqlInit")
        try:
            results = self._sparql.query().convert()
            print(results)
        except Exception as ex:
            logger.exception('SparqlInit exception: ')

    def rdfParser(self, param_format):
        logger.info("RDF Parser")
        try:
            graph = Graph()
            #format is xml not rdf
            print(self._filename)
            graph.parse(self._filename, format=param_format)
            print(len(graph))
            import pprint
            for stmt in graph:
                pprint.pprint(stmt)
        except Exception as ex:
            logger.exception('RDF Parser error:')


    def sparqlQueryForLocalSource(self):
        try:
            logger.info("sparqlQueryForLocalSource")
            print(self._paramFormat)
            print(self._filename)
            print(self._setQuery)
            graph = rdflib.Graph()
            graph.load(self._filename, format=self._paramFormat)
            preparedQuery = prepareQuery(self._setQuery)
            qresult = graph.query(preparedQuery)
            print(type(qresult))
            for row in qresult:
                print(str(row))
        except Exception as ex:
            logger.exception('Sparql for local source exception: ')
        return qresult

    def sparqlQueryRemote(self):
        time.sleep(5)
        results =  self._sparql.query().convert()
        time.sleep(5)
        return results


