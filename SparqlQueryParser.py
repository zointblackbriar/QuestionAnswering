from SPARQLWrapper import SPARQLWrapper, JSON

sparqlEndpoint = SPARQLWrapper("http://dbpedia.org/sparql")

predefined_SPARQL_Who_Is = """PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
                              PREFIX dbpedia: <http://dbpedia.org/resource>
                              PREFIX dbpprop: <http://dbpedia.org/property>
                              
                              SELECT DISTINCT ?person ?comment ?label
                              WHERE {
                                    ?person rdf:type dbpedia-owl:Person.
                                    ?person rdfs:comment ?comment.
                                    ?person rdfs:label ?label
                                    FILTER regex(?label, "^%s", "i")
                                    FILTER (LANG(?comment) = 'en')
                              }
                              LIMIT 1
                            """

predefined_SPARQL_Where_Born = """ PREFIX dbo: <http://dbpedia.org/ontology/>
                                   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                   
                                   SELECT *
                                   WHERE {
                                        ?person rdf:type dbo:Person.
                                        ?person rdfs:label ?label.
                                        ?person dbo:birthPlace ?country.
                                        ?country rdfs:label ?birthPlace.
                                        FILTER regex(?label, "^%s", "i")
                                        FILTER (LANG(?comment) = 'en')

                                   }
                                   LIMIT 1
                               """

predefined_SPARQL_What_Is = """ PREFIX w3-owl: <http://www.w3.org/2002/07/owl#>
                                SELECT ?thing, ?comment, ?label
                                    WHERE {
                                        ?thing rdf:type w3-owl:Thing.
                                        ?thing rdfs:comment ?comment.
                                        ?thing rdfs:label ?label.
                                        FILTER regex(?label, "^%s", "i")
                                        FILTER (LANG(?comment) = 'en')
                                    }
                                    LIMIT 1
                    """

predefined_SPARQL_Where = """     PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
                                  PREFIX dbo: <http://dbpedia.org/ontology/>
                                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                  PREFIX dbp: <http://dbpedia.org/property/>
                                  SELECT *
                                  WHERE  { 
                                    ?location rdf:type dbo:Location.
                                    ?location dbo:location ?country.
                                    ?location rdfs:label ?label.
                                    OPTIONAL {
                                      ?country dbp:coordinatesType ?city.
                                    }
                                    ?country rdfs:label ?countryLabel.
                                    FILTER regex(?label, "^%s", "i")
                                    FILTER (LANG(?comment) = 'en')  
                                  }
                                  LIMIT 1
                    """

# To interrogate who is .... question type
def WhoIsFunc(param):
    sparqlQuery = predefined_SPARQL_Who_Is  % ''.join((param))
    sparqlEndpoint.setQuery(sparqlQuery)
    sparqlEndpoint.setReturnFormat(JSON)
    results = sparqlEndpoint.query().convert()

    #print out results
    if results is None:
        print("No result")
    else:
        for result in results["results"]["bindings"]:
            print(result["comment"]["value"])

def whereIsFunc(param):
    sparqlQuery = predefined_SPARQL_Where % ''.join(param)
    sparqlEndpoint.setQuery(sparqlQuery)
    sparqlEndpoint.setReturnFormat(JSON)
    results = sparqlEndpoint.query().convert()

    for results in results["results"]["bindings"]:
        print(results["countryLabel"]["value"])

def whatIsFunc(param):
    sparqlQuery = predefined_SPARQL_What_Is % ''.join((param))
    sparqlEndpoint.setQuery(sparqlQuery)
    sparqlEndpoint.setReturnFormat(JSON)
    results = sparqlEndpoint.query().convert()

    for results in results["results"]["bindings"]:
        print(results["comment"]["value"])


def whichProperty(param):
    pass