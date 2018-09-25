from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3
#We should add following library. Otherwise, there will be an exception
from rdflib import Graph


predefinedSelectQuery = """PREFIX rdfs: <http://www.w3.org//2000/01/rdf-schema#>
                      SELECT ?label  endpoint = "http://dbpedia.org/sparql"

                      WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }"""

predefinedAskQuery = """ ASK WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label "Asturias"@en }"""

predefinedConstructQuery = """PREFIX dbo: <http://dbpedia.org/ontology/>
                              PREFIX schema: <http://schema.org/>
                              CONSTRUCT {
                                    ?lang a schema:Language;
                                    schema;alternateName ?iso6391Code .
                              }
                              WHERE {
                                    ?lang a dbo:Language;
                                    dbo:iso6391Code ?iso6391Code .
                                    FILTER (STRLEN(?iso6391Code)=2) #to filter out non-valid values
                              } """

predefinedDescribeQuery = """ DESCRIBE <http://dbpedia.org/resource/Asturias> """

def selectQuery(paramSelect):
    #We will use this source for generic question answering
    #SELECT Query
    sparql = SPARQLWrapper(endpoint)
    print("dbpedia sparql endpoint")
    print("predefined query: ", paramSelect)
    sparql.setQuery(paramSelect)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print("results are ready")

    for result in results["results"]["bindings"]:
        print("result: ", result["label"]["value"])

def askQuery(paramAsk):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(paramAsk)
    sparql.setReturnFormat(XML)
    results = sparql.query().convert()
    print("Results in XML: ", results.toxml())

def constructQuery(paramConstruct):
    try:
        sparql = SPARQLWrapper(endpoint)
        sparql.setQuery(predefinedConstructQuery)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results.serialize(format='json'))
    except:
        raise("This query throws an exception")

def describeQuery(paramDescribe):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(predefinedDescribeQuery)
    sparql.setReturnFormat(N3)
    results = sparql.query().convert()
    g = Graph()
    g.parse(data=results, format="n3")
    print(g.serialize(format='n3'))

