from SPARQLWrapper import SPARQLWrapper, JSON
import logging
import colored_logs
from rdflib.graph import Graph
from rdflib.plugins import sparql
from rdflib.namespace import FOAF
from rdflib.plugins.sparql.prepareQuery import prepareQuery


logger = logging.getLogger(__name__)

# Add console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
cf = colored_logs.ColoredFormatter("[%(name)s][%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)")
ch.setFormatter(cf)
logger.addHandler(ch)

# Set log level
logger.setLevel(logging.DEBUG)

# setPrefix = "@prefix factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#> . \
# @prefix : <http://linkedfactory.iwu.fraunhofer.de/data/> . \
# @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . \
# @prefix owl: <http://www.w3.org/2002/07/owl#> . \
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#> . \
# @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ."
queryShowEverything = "SELECT * { ?s ?p ?o }"
queryCountAllRDF = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
testQuery = "SELECT * { ?s ?factory:contains ?sensor5 } "


class SPARQLEndpoint(object):

    def __init__(self, endpoint, setQuery, filename="data/energy.rdf"):
        self._endpoint = endpoint
        self._setQuery = setQuery
        self._filename = filename


    def SparqlInit(self):
        logger.info("SparqlInit")
        try:
            sparql = SPARQLWrapper(self._endpoint)
            sparql.setQuery(self._setQuery)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            print(results)

            # for result in results["results"]["bindings"]:
            #     print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))
        except Exception as ex:
            logger.error('Failed while parsing: ' + str(ex))

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
            logger.error('Failed while sending a query:', str(ex))

    def sparqlQueryForLocalSource(self, param_format, param_namespace):
        logger.info("sparqlQueryForLocalSource")
        try:
            graph = Graph()
            graph.load(self._filename, format=param_format)
            #graph.parse(self._filename)
            qresult = graph.query(self._setQuery, initNs={ 'foaf': FOAF })
            #qresult = prepare
            print(qresult)
            # for row in qresult:
            #     print (rdflib.term.Literal(row).value)
            import pprint
            for statement in graph:
                pprint.pprint(statement)

        except Exception as  ex:
            logger.error('Failed while sending a query:', str(ex))

print(queryShowEverything)
endpointObjectHolder = SPARQLEndpoint("http://linkedfactory.iwu.fraunhofer.de/",
                                      queryShowEverything, "data/testFraunhoferData.ttl")

#endpointObjectHolder.SparqlInit()
#endpointObjectHolder.rdfParser('ttl')
endpointObjectHolder.sparqlQueryForLocalSource('ttl', { 'foaf': FOAF })


