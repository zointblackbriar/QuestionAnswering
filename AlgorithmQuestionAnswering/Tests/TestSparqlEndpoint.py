import os
os.chdir(r'../')


import SparqlEndpoint
import unittest
from io import StringIO
import sys
import time

# Todo write a test suite
parameterizedQuery = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                  PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  PREFIX owl: <http://www.w3.org/2002/07/owl#>
                  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  SELECT ?s ?o WHERE {
                   <http://linkedfactory.iwu.fraunhofer.de/""" + """linkedfactory""" + """>""" + """ factory:contains ?o . }"""

inversedQuery = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                  PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  PREFIX owl: <http://www.w3.org/2002/07/owl#>
                  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  SELECT ?s ?o WHERE {
                    ?s  factory:contains <http://linkedfactory.iwu.fraunhofer.de/linkedfactory/IWU/FoFab/NSHV/Versuchsfeld/UV1> . }"""

#Extract labels and comments from a rdf source
rdfExtractor = """PREFIX ns: <http://oaei.ontologymatching.org/2011/benchmarks/101/onto.rdf#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                
                SELECT DISTINCT ?varClass ?varSubClass ?varSubClassComment ?varProperty ?varPropComment
                FROM <http://oaei.ontologymatching.org/2011/benchmarks/101/onto.rdf>
                WHERE {
                  VALUES ?propertyType { owl:ObjectProperty owl:DatatypeProperty }
                
                  ?varClass rdf:type owl:Class .
                  ?varProperty rdf:type ?propertyType ;
                               rdfs:domain ?varClass .
                  OPTIONAL{ ?varProperty rdfs:comment ?varPropComment }
                  OPTIONAL{ ?varSubClass rdfs:subClassOf ?varClass ;
                                         rdfs:comment ?varSubClassComment }
                }
"""

#To get all of information
exploratoryPropertyQuery = """ SELECT DISTINCT ?property
                        WHERE {
                          ?s ?property ?o .
                          OPTIONAL { ?s ?p rdfs:label. }
                        } 
                    """

exploratoryObjectQuery = """SELECT DISTINCT ?object
                        WHERE {
                          ?s ?p ?object .
                          OPTIONAL { ?s ?p rdfs:label. }
                        } 
                    """

selectWithName = """SELECT DISTINCT ?object
                    WHERE {
                        ?s ?:BrowseName ?object .
                        """

class BaseTestClass(unittest.TestCase):

    @unittest.skip("Last query will be tested")
    def test_query_results(self):
        test_query = "SELECT * WHERE {?s ?p ?o. }"
        obj = SparqlEndpoint.SPARQLEndpoint("localhost", test_query, "ttl", filename="SemanticSource/FraunhoferData.ttl")
        result = obj.sparqlQueryForLocalSource()
        time.sleep(3)
        listResult = []
        for row in result:
            print(row)
            listResult.append(row)
        self.assertEqual(listResult[0], """(rdflib.term.URIRef(u'http://linkedfactory.iwu.fraunhofer.de/linkedfactory/IWU/FoFab/GLT/Elektrische_Energie'), rdflib.term.URIRef(u'http://linkedfactory.iwu.fraunhofer.de/vocab#contains'), rdflib.term.URIRef(u'http://linkedfactory.iwu.fraunhofer.de/linkedfactory/IWU/FoFab/GLT/Elektrische_Energie/Abgang_MSR')""")

    @unittest.skip("Last query will be tested")
    def test_combined_results(self):
        test_query = parameterizedQuery + """union """ + inversedQuery
        obj = SparqlEndpoint.SPARQLEndpoint("localhost", test_query, "ttl", filename="SemanticSource/FraunhoferData.ttl")
        results = obj.sparqlQueryForLocalSource()
        time.sleep(3)
        for row in results:
            results.append(row)
        self.assertEqual(results, ['hello'])

    @unittest.skip("Last query will be tested")
    def test_iwu_test_rack(self):
        test_query = exploratoryPropertyQuery
        comparison = []
        endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", test_query, "ttl", filename="SemanticSource/IWU_TestRack.ttl")
        results = endpoint.sparqlQueryForLocalSource()
        time.sleep(3)
        for row in results:
            comparison.append(row)
        print("comparison results: ", type(comparison[0]))
        self.assertFalse(isinstance(comparison[0], str))

    @unittest.skip("Last query will be tested")
    def test_iwu_test_rack_objects(self):
        test_query = exploratoryObjectQuery
        comparison = []
        endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", test_query, "ttl", filename="SemanticSource/IWU_TestRack.ttl")
        results = endpoint.sparqlQueryForLocalSource()
        time.sleep(3)
        for row in results:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    @unittest.skip("Last query will be tested")
    def test_montage_demonstrator_properties(self):
        test_query = exploratoryPropertyQuery
        comparison = []
        endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", test_query, "ttl", filename="SemanticSource/montagedemonstrator_modul1.ttl")
        results = endpoint.sparqlQueryForLocalSource()
        time.sleep(3)
        for row in results:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    @unittest.skip("Last query will be tested")
    def test_opc_generated_data_questy(self):
        test_query = exploratoryPropertyQuery
        comparison = []
        endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", test_query, "ttl", filename = "SemanticSource/OPCGeneratedData.ttl")
        results = endpoint.sparqlQueryForLocalSource()
        time.sleep(3)
        for row in results:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    # def test_opc_generated_access_level_query(self):
    #     test_query = """ PREFIX access: <http://opcfoundation.org/UA/2011/03/UANodeSet.xsd>
    #                     SELECT DISTINCT ?property
    #                     WHERE {
    #                       ?s ?access#AccessLevel ?o .
    #                       OPTIONAL { ?s ?p rdfs:label. }
    #                     }
    #                 """
    #     comparison = []
    #     endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", test_query, "ttl", filename = "SemanticSource/OPCGeneratedData.ttl")
    #     with self.assertEqual(IndexError):
    #         results = endpoint.sparqlQueryForLocalSource()
    #         time.sleep(3)
    #         for row in results:
    #             comparison.append(row)
    #             break
    #         self.assertFalse(isinstance(comparison[0], str))

    @unittest.skip("Last query will be tested")
    def test_complex_optional_query_generated_data(self):
        selectOptional = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            SELECT DISTINCT ?object
                            WHERE {
                                ?s rdf:value ?object . 
                                }
                                """
        comparison = []
        endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", selectOptional, "ttl", filename = "SemanticSource/OPCGeneratedData.ttl")
        results = endpoint.sparqlQueryForLocalSource()
        time.sleep(3)
        for row in results:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    @unittest.skip("Last query will be tested")
    def test_complex_browse_name_query_generated_data(self):
        selectOptional = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                              PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                              PREFIX owl: <http://www.w3.org/2002/07/owl#>
                              PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                              PREFIX : <http://opcfoundation.org/UA/2011/03/UANodeSet.xsd#> 

                            SELECT DISTINCT ?object
                            WHERE {
                                ?s :BrowseName ?object . 
                                }
                                """
        comparison = []
        endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", selectOptional, "ttl", filename = "SemanticSource/OPCGeneratedData.ttl")
        results = endpoint.sparqlQueryForLocalSource()
        time.sleep(3)
        for row in results:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    @unittest.skip("Last query will be tested")
    def test_lf_contains_browse_query_generated_data(self):
        combinedQuery = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                              PREFIX owl: <http://www.w3.org/2002/07/owl#>
                            PREFIX lf: <http://linkedfactory.org/vocab/> 
                            PREFIX lf-plc: <http://linkedfactory.org/vocab/plc/> 
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
                              PREFIX : <http://opcfoundation.org/UA/2011/03/UANodeSet.xsd#> 

                            SELECT DISTINCT ?object
                            WHERE {
                                ?s lf:contains ?object . 
                                }
                                """
        comparison = []
        endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", combinedQuery, "ttl", filename = "SemanticSource/OPCGeneratedData.ttl")
        results = endpoint.sparqlQueryForLocalSource()
        time.sleep(3)
        for row in results:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))

    def test_station_data(self):
        #?s rdf:type ?o .
        #                                   } } UNION
        #                          { SELECT ?object
        #                           WHERE
        #                           {
        #                               ?s rdf:type ?o .
        #                                lf-plc:CPU ?object .
        #                           } }
        #                         }
        #                                  ?s rdf:type ?o;

        combinedQuery = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                                             PREFIX : <http://opcfoundation.org/UA/2011/03/UANodeSet.xsd#> 
                                             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                             PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                             PREFIX lf: <http://linkedfactory.org/vocab/> 
                                             PREFIX lf-plc: <http://linkedfactory.org/vocab/plc/> 
                                             SELECT DISTINCT *
                                WHERE { 
                                    ?s rdf:type ?o .
                                    ?s lf-plc:Station ?o .
                                UNION {
                                     SELECT * WHERE { ?s rdfs:label ?o . } 
                                    }"""
        comparison = []
        endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", combinedQuery, "ttl", filename = "SemanticSource/OPCGeneratedData.ttl")
        results = endpoint.sparqlQueryForLocalSource()
        time.sleep(3)
        for row in results:
            comparison.append(row)
        self.assertFalse(isinstance(comparison[0], str))




class OutputBuffer(object):

    def __init__(self):
        self.stdout = StringIO()
        self.stderr = StringIO()

    def __entr__(self):
        self.original_stdout, self.original_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self.stdout, self.stderr

    def __exit__(self, exception_type, exception, traceback):
            sys.stdout, sys.stderr = self.original_stdout, self.original_stderr

    @property
    def out(self):
        return self.stdout.getvalue()

    @property
    def err(self):
        return self.stderr.getvalue()

if __name__ == '__main__':
    unittest.main()