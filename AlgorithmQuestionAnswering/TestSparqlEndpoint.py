import SparqlEndpoint


#Todo write a test suite
parameterizedQuery = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                  PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  PREFIX owl: <http://www.w3.org/2002/07/owl#>
                  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  SELECT ?s ?o WHERE {
                   <http://linkedfactory.iwu.fraunhofer.de/""" + """linkedfactory""" +  """>""" + """ factory:contains ?o . }"""

inversedQuery = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                  PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  PREFIX owl: <http://www.w3.org/2002/07/owl#>
                  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  SELECT ?s ?o WHERE {
                    ?s  factory:contains <http://linkedfactory.iwu.fraunhofer.de/linkedfactory/IWU/FoFab/NSHV/Versuchsfeld/UV1> . }"""

test_query = "SELECT * WHERE {?s ?p ?o. }"

obj = SparqlEndpoint.SPARQLEndpoint("", inversedQuery, "ttl", "DataSource/FraunhoferData.ttl")
result = obj.sparqlQueryForLocalSource()
for row in result:
    print(row)
