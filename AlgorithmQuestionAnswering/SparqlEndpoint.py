#!/usr/bin/env python
# coding: utf-8


from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from rdflib.graph import Graph
from rdflib.plugins import sparql
from rdflib import URIRef
from rdflib.plugin import register, Serializer, Parser
register('ttl', Parser, 'rdflib.plugins.parsers.notation3', 'TurtleParser')
import logging
import colored_logs
import time


logging.info('Starting logger for ...') #or call logging.basicConfig
# Set log name
logger = logging.getLogger(__name__)


# containmentQuery = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
#                       PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
#                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#                       PREFIX owl: <http://www.w3.org/2002/07/owl#>
#                       PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#                       PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#                       SELECT ?s ?o WHERE {
#                        <http://linkedfactory.iwu.fraunhofer.de/linkedfactory>  factory:contains ?o . }"""

class SPARQLEndpoint():

    #default energy.rdf
    def __init__(self, endpoint, setQuery, paramFormat, filename=None):
        self._endpoint = endpoint
        self._setQuery = setQuery
        self._paramFormat = paramFormat
        self._filename = filename
        self._sparql = SPARQLWrapper(self._endpoint)



    def SparqlInit(self):
        logger.info("SparqlInit")
        try:
            # sparql = SPARQLWrapper(self._endpoint)
            # sparql.setQuery(self._setQuery)
            # sparql.setReturnFormat(JSON)
            results = self._sparql.query().convert()
            print(results)

            # for result in results["results"]["bindings"]:
            #     print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))
        except Exception as ex:
            logger.exception('SparqlInit exception: ')

    def rdfParser(self, param_format):
        logger.info("RDF Parser")
        try:
            graph = Graph()
            #format is xml not rdf
            print(self._filename)
            graph.parse(self._filename, format=param_format)
            #getURIRef = URIRef('http://linkedfactory.iwu.fraunhofer.de')
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
            #graph.parse(self._filename, param_format)
            qresult = graph.query(self._setQuery)
            #qresult = graph.serialize(format='ttl')
            # for row in qresult:
            #     print(row)
            # import pprint
            # for statement in graph:
            #     pprint.pprint(statement)
        except Exception as ex:
            logger.exception('Sparql for local source exception: ')
        return qresult

    def sparqlQueryRemote(self):
        #self._sparql.setReturnFormat(JSON)
        time.sleep(5)
        results =  self._sparql.query().convert()
        time.sleep(5)
        return results
        #resultsRemote = self._sparql.query().convert()
        #print(resultsRemote)


parameterizedQuery = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                  PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  PREFIX owl: <http://www.w3.org/2002/07/owl#>
                  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  SELECT ?s ?o WHERE {
                   <http://linkedfactory.iwu.fraunhofer.de/""" + """linkedfactory""" +  """>""" + """ factory:contains ?o . }"""

test_query = "SELECT * WHERE {?s ?p ?o. }"

#The following code for test purpose
#endpointRemote = SPARQLEndpoint("localhost", parameterizedQuery, "ttl", filename="DataSource/FraunhoferData.ttl")
#time.sleep(3)
#endpointRemote.sparqlQueryForLocalSource()
#resultSparqlQuery = endpointRemote.sparqlQueryForLocalSource('ttl')
