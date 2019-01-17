import unittest
import os
os.chdir(r'../')

import SparqlEndpoint
import time
import StanfordSpacyNLP
import SPARQLGenerator


# test_query = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
#           PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
#           PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#           PREFIX owl: <http://www.w3.org/2002/07/owl#>
#           PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#           SELECT ?s ?o
#                   WHERE {
#                     { <http://linkedfactory.iwu.fraunhofer.de/linkedfactory/IWU/FoFab/BHKW> factory:contains ?o }
#                      UNION { <http://linkedfactory.iwu.fraunhofer.de/linkedfactory> factory:contains ?o  }
#                      UNION { <http://linkedfactory.iwu.fraunhofer.de/linkedfactory/IWU/FoFab/GLT> factory:contains ?o  }
#                 }
#             """

class BaseTestClass(unittest.TestCase):
    def test_union_first(self):
        test_query = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                  PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  PREFIX owl: <http://www.w3.org/2002/07/owl#>
                  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  SELECT ?s ?o 
                          WHERE {
                            { <http://linkedfactory.iwu.fraunhofer.de/linkedfactory/IWU/FoFab/BHKW> factory:contains ?o }
                             UNION { <http://linkedfactory.iwu.fraunhofer.de/linkedfactory> factory:contains ?o  }
                             UNION { <http://linkedfactory.iwu.fraunhofer.de/linkedfactory/IWU/FoFab/GLT> factory:contains ?o  }
                        }                   
                    """

        endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", test_query, "ttl", filename="SemanticSource/FraunhoferData.ttl")
        result = endpoint.sparqlQueryForLocalSource()
        time.sleep(5)
        listResult = []
        for row in result:
            print(row)
            listResult.append(row)
            self.assertFalse(isinstance(listResult, str))

    def test_question_union_first(self):
        input = "What do linkedfactory, iwu, powermeter and aximus contain?"
        self.assertFalse(isinstance(self.query_perform(input), str))

    def test_question_union_second(self):
        input = "What do linkedfactory, iwu  contain?"
        self.assertFalse(isinstance(self.query_perform(input), str))

    def test_question_union_third(self):
        input = "What does fofab contain?"
        self.assertFalse(isinstance(self.query_perform(input), str))

    def test_question_union_fourth(self):
        input = "contain fofab and linkedfactory"
        self.assertFalse(isinstance(self.query_perform(input), str))



    def query_perform(self, input):
        #input = "What do linkedfactory, iwu, powermeter and aximus contain?"
        nlpTask = StanfordSpacyNLP.TestConnectionCoreNLP()
        resultOfConstituentParse = nlpTask.constituencyParser(input)
        print(resultOfConstituentParse.pretty_print())
        print(resultOfConstituentParse.leaves())

        verb = []
        noun = []
        verb = nlpTask.spacyArchMatching(input)
        noun = nlpTask.findNNSubtree(resultOfConstituentParse)
        wordnetLatentAnalysis = nlpTask.wordnetLatentAnalysis(str(verb[-1]), 'contains')
        directedFlag = nlpTask.spacyDependencyChunk(input)
        print("noun", noun)
        print("verb", verb)
        print("length of noun", len(noun))
        if(len(noun) > 1):
            #add a counter
            prefixEdit = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                                             PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                                             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                             PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"""
            union_part = """ UNION { <http://linkedfactory.iwu.fraunhofer.de/"""

            parameterizedQuery = prefixEdit + """
                                         SELECT DISTINCT ?s ?o WHERE {
                                          { <http://linkedfactory.iwu.fraunhofer.de/"""

            parameterized_first_part = parameterizedQuery + str(SPARQLGenerator.SPARQLGeneratorClass.add_path_to_IRI(
                noun[0])) + """>""" + """ factory:contains ?o . }"""

            for member in noun:
                if member == noun[0]:
                    continue
                parameterizedQuery = union_part + str(SPARQLGenerator.SPARQLGeneratorClass.add_path_to_IRI(
                    member)) + """>""" + """ factory:contains ?o . }"""
                parameterized_first_part += parameterizedQuery
            parameterized_first_part += " } "

            print(parameterized_first_part)

            endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", parameterized_first_part, "ttl", filename="SemanticSource/FraunhoferData.ttl")
            result = endpoint.sparqlQueryForLocalSource()
            time.sleep(5)
            listResult = []
            for row in result:
                print(row)
                listResult.append(row)
                self.assertFalse(isinstance(listResult[0], str))
        else:
            prefixEdit = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                                             PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                                             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                             PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"""
            parameterizedQuery = prefixEdit + """
                                             SELECT DISTINCT ?s ?o WHERE {
                                              <http://linkedfactory.iwu.fraunhofer.de/"""

            parameterizedQuery = parameterizedQuery + str(SPARQLGenerator.SPARQLGeneratorClass.add_path_to_IRI(noun[-1])) + """>""" + """ factory:contains ?o . }"""
            endpoint = SparqlEndpoint.SPARQLEndpoint("localhost", parameterizedQuery, "ttl", filename="SemanticSource/FraunhoferData.ttl")
            result = endpoint.sparqlQueryForLocalSource()
            time.sleep(5)
            list_result = []
            for row in result:
                print(row)
                list_result.append(row)
            return list_result






if __name__ == '__main__':
    unittest.main()