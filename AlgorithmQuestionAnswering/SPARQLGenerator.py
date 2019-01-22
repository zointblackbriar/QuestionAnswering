#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from StanfordSpacyNLP import ConnectionCoreNLP, TestConnectionCoreNLP
from QuestionClassification import QuestionClassifier
from SparqlEndpoint import SPARQLEndpoint
from NLTKProp import NLTKProp
from QuestionClassification import QuestionClassificationSVM
import Utils
#import StanfordSpacyNLP
import re
import time
import logging
import json, ast
import os

logging.info('Starting logger for ...') #or call logging.basicConfig
# Set log name
logger = logging.getLogger(__name__)


obj = ConnectionCoreNLP()
nlpTask = TestConnectionCoreNLP()

# all_properties_query = prefix_query + """ SELECT DISTINCT ?property
#                 WHERE {
#                   ?s ?property ?o .
#                   OPTIONAL { ?s ?p rdfs:label. }
#                 }
#             """

# a question for average value
# a sample dynamic query
# queryDynamicAverage = """SELECT (AVG(?value) AS ?avg)
#        (MIN(?value) AS ?min)
#        (MAX(?value) AS ?max)
# WHERE {
# service <kvin:> {  <http://localhost:10080/""" + path + """/""" + matchedContext[machineIndex[0]] + """/""" +  matchedContext[sensorIndex[0]] + """> <http://example.org/value> ?v . ?v <kvin:limit> 10000; <kvin:value> ?value} }"""


#os.chdir(r'../')
#print(os.getcwd())
EN_MODEL_MD = "en_core_web_md"

class SPARQLGeneratorClass():

    def __init__(self):
        pass

    def SPARQLGenerate(self, input):
        listOfPostTagger = obj.parse(input)
        print("list of Post Tagger", listOfPostTagger)



    def sampleTestChromeDriver(self):
        driver = webdriver.Chrome('C:\\ProgramData\\chocolatey\\lib\\chromedriver\\tools\\chromedriver.exe')  # Optional argument, if not specified will search path.
        driver.get('http://www.google.com/xhtml')
        time.sleep(5)  # Let the user actually see something!
        search_box = driver.find_element_by_name('q')
        search_box.send_keys('ChromeDriver')
        search_box.submit()
        time.sleep(5)  # Let the user actually see something!
        driver.quit()

    """Method: queryTestingSelenium is a method for taking data from KVIN Service in the case of non-existing normative SPARQL endpoing."""
    # Arguments
    #     sparqlQuery: It takes a SPARQL query in order to give an answer to a user
    # Output
    #     Returns RDF triples as a dictionary of Python format

    @staticmethod
    #We will use selenium tool to reach SPARQL Endpoint
    def queryTestingSelenium(sparqlQuery):
        try:
            dictionary = {}
            options = webdriver.ChromeOptions()
            #headless is a chromium option for silenty working
            options.add_argument("headless")
            driver = webdriver.Chrome('C:\\ProgramData\\chocolatey\\lib\\chromedriver\\tools\\chromedriver.exe', chrome_options=options)  # Optional argument, if not specified will search path.
            driver.get('http://localhost:10080/sparql')
            time.sleep(2)
            text_area = driver.find_element_by_id('query')
            select = Select(driver.find_element_by_id('model'))
            select.select_by_visible_text('<http://linkedfactory.iwu.fraunhofer.de/data/>')
            #or you can change with the following case
            # <enilink:model:users>
            #select = Select(driver.find_element_by_name('<enilink:model:users>'))
            text_area.send_keys(sparqlQuery)
            driver.find_element_by_id('#submitBtn').click()
            time.sleep(3)
            print('Result is printed out')
            #table = driver.find_element_by_css_selector(".table.table-hover")
            table = driver.find_element_by_css_selector(".table-hover")
            head = driver.find_element_by_tag_name('thead')
            body=driver.find_element_by_tag_name('tbody')
            elements = []
            headerTag = []
            body_line = body.find_element_by_tag_name("tr")
            elements = [item.text.encode("utf8") for item in body_line.find_elements_by_tag_name('td')]
            headerTag = [item.text.encode("utf8") for item in head.find_elements_by_tag_name('th')]
            elements.append(",".join(elements))
            headerTag.append(",".join(headerTag))
            print("elements", elements)
            print("headerTag", headerTag)
            #combine elements and headerTag into a single dictionary
            dictionary = dict(zip(headerTag, elements))
            print("dictionary", dictionary)
            print('Driver quit')
            driver.quit()

        except Exception as ex:
            logger.exception("When query sent to selenium, an error occurred")
        return dictionary

    @staticmethod
    def switch_case_opc_generated(item):
        item = item.lower()
        switcher = {
            "stationmanager": "http://example.org/SIMATIC_HMI-Station(1)/Stationmanager1-S7-Programm(1"
        }
        return switcher.get(item)

    """Method: add_path_to_IRI is a path adder into IRIs of Turtle files."""
    # Arguments
    #     item: the string path to be added into IRIs
    # Output
    #     Returns a compact IRIs into question answering
    @staticmethod
    def add_path_to_IRI(item):
        item  = item.lower()
        switcher = {
            "linkedfactory": """linkedfactory""",
            "e3sim": """linkedfactory/IWU/E3-Sim""",
            "iwu": """linkedfactory/IWU""",
            "fofab": """linkedfactory/IWU/E3-Sim/FoFab""",
            "bhkw": """linkedfactory/IWU/FoFab/BHKW""",
            "glt": """linkedfactory/IWU/FoFab/GLT""",
            "kälte" or "kaelte": """linkedfactory/IWU/FoFab/GLT/Kälte""",
            "wärme" or "waerme": """linkedfactory/IWU/FoFab/Wärme""",
            "gmx": """linkedfactory/IWU/FoFab/GMX""",
            "nshv": """linkedfactory/IWU/FoFab/NSHV""",
            "versuchsfeld": """linkedfactory/IWU/FoFab/NSHV/Versuchsfeld""",
            "elektrische_energie": """linkedfactory/IWU/FoFab/GLT/Elektrische_Energie""",
            "rollex": """linkedfactory/IWU/FoFab/Rollex""",
            "powermeter": """linkedfactory/IWU/FoFab/Rollex/PowerMeter""",
            "solarplant": """linkedfactory/IWU/FoFab/PowerMeter""",
            #TODO: the following will be handled with NLP
            "rollexiwu": """linkedfactory/IWU/Rollex""",
            "rollexiwupowermeter": """linkedfactory/IWU/Rollex/PowerMeter""",
            #TODO is gonna realize till here
            "demofactory": """linkedfactory/demofactory""",
            "machine1": """linkedfactory/demofactory/machine1""",
            "machine2": """linkedfactory/demofactory/machine2""",
            "machine3": """linkedfactory/demofactory/machine3""",
            "machine4": """linkedfactory/demofactory/machine4""",
            "machine5": """linkedfactory/demofactory/machine5""",
            "machine6": """linkedfactory/demofactory/machine6""",
            "machine7": """linkedfactory/demofactory/machine7""",
            "machine8": """linkedfactory/demofactory/machine8""",
            "machine9": """linkedfactory/demofactory/machine9""",
            "machine10": """linkedfactory/demofactory/machine10""",
            #inversed query
            "aximus": """linkedfactory/IWU/E3-Sim/FoFab/Aximus""",
            "bdm2000": """linkedfactory/IWU/E3-Sim/FoFab/BDM2000""",
            "fliesspressen": "linkedfactory/IWU/E3-Sim/FoFab/Fliesspressen",
            "gmxentgraten": "linkedfactory/IWU/E3-Sim/FoFab/GMX_Entgraten",
            "gmxspanen1": "linkedfactory/IWU/E3-Sim/FoFab/GMX_Spanen1",
            "gmxspanen2": "linkedfactory/IWU/E3-Sim/FoFab/GMX_Spanen2",
            "gmxspanen3": "linkedfactory/IWU/E3-Sim/FoFab/GMX_Spanen3",
            "gmxspanen4": "linkedfactory/IWU/E3-Sim/FoFab/GMX_Spanen4",
            "gmxpanen5": "linkedfactory/IWU/E3-Sim/FoFab/GMX_Spanen5",
            "ha100": "linkedfactory/IWU/E3-Sim/FoFab/HA100",
            "karobau": "linkedfactory/IWU/E3-Sim/FoFab/Karobau",
            "prd40": "linkedfactory/IWU/E3-Sim/FoFab/PDR40",
            "pwz": "linkedfactory/IWU/E3-Sim/FoFab/PWZ",
            "querwalzen": "linkedfactory/IWU/E3-Sim/FoFab/Querwalzen",
            "nshvbuero" or "nshvbüro": "linkedfactory/IWU/E3-Sim/FoFab/GMX_Spanen1",
            "coolingwater": "linkedfactory/IWU/FoFab/BHKW/CoolingWater",
            "emergencycooling": "linkedfactory/IWU/FoFab/BHKW/EmergencyCooling",
            "generator": "linkedfactory/IWU/FoFab/BHKW/Generator",
            "heatmeter": "linkedfactory/IWU/FoFab/BHKW/HeatMeter",
            "heatingwater": "linkedfactory/IWU/FoFab/BHKW/HeatingWater",
            "uv1": "linkedfactory/IWU/FoFab/NSHV/Versuchsfeld/UV1",
            "uv2": "linkedfactory/IWU/FoFab/NSHV/Versuchsfeld/UV2",
            "uv3": "linkedfactory/IWU/FoFab/NSHV/Versuchsfeld/UV3",
            "uv4": "linkedfactory/IWU/FoFab/NSHV/Versuchsfeld/UV4",
            "uv5": "linkedfactory/IWU/FoFab/NSHV/Versuchsfeld/UV5",
            "uv6": "linkedfactory/IWU/FoFab/NSHV/Versuchsfeld/UV6",
            "WRTE5K69:314605750": "linkedfactory/IWU/FoFab/SolarPlant/WRTE5K69:314605750",
            "WRTE5K69:314605751": "linkedfactory/IWU/FoFab/SolarPlant/WRTE5K69:314605751",
            "WRTP4675:2110426305": "linkedfactory/IWU/FoFab/SolarPlant/WRTP4675:2110426305"

        }
        return switcher.get(item)

    """Method: static_query_triples method is used for fetching data from static semantic sources defined by linkedfactory or enilink"""
    # Arguments
    #     input_text: a question or keyword based search items for question answering system.
    # Output shape
    #     It will give us a results in dictionary format for static input
    @staticmethod
    def static_query_triples(input_text):
        #for checkbox
        resultOfConstituentParse = ""
        stanford_parser = TestConnectionCoreNLP()
        resultOfConstituentParse = stanford_parser.constituencyParser(input_text)
        print(resultOfConstituentParse.pretty_print())
        print(resultOfConstituentParse.leaves())

        print("input text: ", type(input_text))
        input_text = str(input_text)
        # questionAnswering = QuestionClassifier.QuestionAssigner.predictQuestion(input_text)
        # if questionAnswering is 'unknown':
        #     return

        verb = []
        noun = []
        #verb = nlpTask.printSubtrees(param_ConstituencyParser, 'VP', 'VBZ')
        verb = nlpTask.spacyArchMatching(input_text)
        #verb = nlpTask.findVPSubtree(param_ConstituencyParser)[0]
        #noun = nlpTask.printSubtrees(param_ConstituencyParser, 'NN', 'NNP')
        noun = nlpTask.findNNSubtree(resultOfConstituentParse)
        #adjective = nlpTask.printSubtrees(resultOfConstituentParse, 'ADJP', 'JJ')
        adjective = nlpTask.printSubtrees(resultOfConstituentParse, 'ADJP')
        print('type of adjective', type(adjective))
        print("adjective", adjective)


        #What does linkedfactory contain?
        #Linkedfactory behaves as adjective
        if(len(noun) == 0):
            print("No noun change with adjective")
            adjective = ast.literal_eval(json.dumps(adjective))
            print("changed adjective", adjective[0])
            noun.append(adjective[0])
            print("changed noun", noun[-1])

        if(noun != None and verb != None):
            print("Noun and verb is not empty")
            noun = ast.literal_eval(json.dumps(noun))
            #verb = ast.literal_eval(json.dumps(verb))
           # print("noun", noun[-1])
            #noun.append(noun)
            print("changed noun", noun)
            print("verb", verb[-1])

        #stemmed_verb = NLTKProp.stemmingSnowball(str(verb[-1]))
        logger.info("check wordnet synonym analysis")
        if(verb != None):
            lemmatized_verb = stanford_parser.spacy_verb_lemmatizer(str(verb[-1]))
            print("lemmatized verb: ", lemmatized_verb)
            #wordnetLatentAnalysis = nlpTask.wordnetLatentAnalysis(str(verb[-1]), 'contains')
            print("type of lemmatized verb: ", type(lemmatized_verb))
            wordnetLatentAnalysis = nlpTask.wordnetLatentAnalysis(str(lemmatized_verb[0]), 'contain')
        indirect_dependency = nlpTask.spacyDependencyChunk(input_text)

        prefixEdit = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                                         PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                                         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                         PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"""
        parameterizedQuery = prefixEdit + """
                                         SELECT ?s ?o WHERE {
                                          <http://linkedfactory.iwu.fraunhofer.de/"""

        resultOFLocalSource = ""

        try:
            #get a verb which has been analyzed and compare with its dependency parse tree against inverse query
            #stemmed_verb == 'contains'
            if (wordnetLatentAnalysis == True) and indirect_dependency == False and len(noun) <= 1:
                logger.info("Contains verb analyzed")
                print("Direct Query")
                parameterizedQuery = parameterizedQuery + str(SPARQLGeneratorClass.add_path_to_IRI(noun[-1])) + """>""" + """ factory:contains ?o . }"""
                print('parameterizedQuery', parameterizedQuery)
                endpointRemote = SPARQLEndpoint("localhost", parameterizedQuery, "ttl", filename="SemanticSource/FraunhoferData.ttl")
                time.sleep(3)
                resultOFLocalSource = endpointRemote.sparqlQueryForLocalSource()

            elif wordnetLatentAnalysis == True and len(noun) > 1:
                print("Union Query")
                parameterizedQuery = prefixEdit + """
                                                 SELECT ?s ?o WHERE {
                                                  { <http://linkedfactory.iwu.fraunhofer.de/"""
                union_part = """ UNION { <http://linkedfactory.iwu.fraunhofer.de/"""

                parameterized_total = parameterizedQuery + str(
                    SPARQLGeneratorClass.add_path_to_IRI(
                        noun[0])) + """>""" + """ factory:contains ?o . }"""
                for member in noun:
                    if member == noun[0]:
                        continue
                    parameterizedQuery = union_part + str(SPARQLGeneratorClass.add_path_to_IRI(
                    member)) + """>""" + """ factory:contains ?o . }"""
                    parameterized_total += parameterizedQuery
                parameterized_total += " } "
                endpoint = SPARQLEndpoint("localhost", parameterized_total, "ttl", filename="SemanticSource/FraunhoferData.ttl")
                resultOFLocalSource = endpoint.sparqlQueryForLocalSource()

            #stemmed_verb == 'contains'
            elif indirect_dependency == True and wordnetLatentAnalysis == True:
                    #nlpTask.wordnetLatentAnalysis(ast.literal_eval(json.dumps(nlpTask.findVPSubtree(param_ConstituencyParser)[0])), "contains"):
                print("Indirect Query")
                inversedQuery = prefixEdit + """ SELECT ?s ?o WHERE { ?s  factory:contains """
                inversedQuery = inversedQuery + """<http://linkedfactory.iwu.fraunhofer.de/""" + str(SPARQLGeneratorClass.add_path_to_IRI(noun[-1])) + """>. }"""
                print("inversedQuery", inversedQuery)
                endpointRemote = SPARQLEndpoint("localhost", inversedQuery, "ttl", filename="SemanticSource/FraunhoferData.ttl")
                time.sleep(3)
                resultOFLocalSource = endpointRemote.sparqlQueryForLocalSource()


            else:
                #noun = ast.literal_eval(json.dumps(noun))
                print("No specific verb - Affirmation Statement")
                if noun[len(noun)-1] != None:
                    #Give me all of members linkedfactory? == linkedfactory - nn
                    parameterizedQuery = parameterizedQuery + str(SPARQLGeneratorClass.add_path_to_IRI(noun[-1])) + """>""" + """ factory:contains ?o . }"""
                    endpointRemote = SPARQLEndpoint("localhost", parameterizedQuery, "ttl",
                                                    filename="SemanticSource/FraunhoferData.ttl")
                    resultOFLocalSource = endpointRemote.sparqlQueryForLocalSource()
        except (Exception):
            logger.exception("parameterized Query has some errors")
        return resultOFLocalSource, resultOfConstituentParse

    """Method: dynamic_query_triples method is used for fetching data from static semantic sources defined by linkedfactory or enilink"""
    # Arguments
    #     input_text: a question or keyword based search items for question answering system.
    # Output shape
    #     It will give us a results in dictionary format for static input

    @staticmethod
    def dynamic_query_triples(input):
        try:
            #The following code will be tested again
            # import QuestionClassification
            # questionAnswering = QuestionClassification.QuestionClassifier.QuestionAssigner.predictQuestion(input)
            # if questionAnswering is 'unknown' or questionAnswering is 'who' or questionAnswering is 'when':
            #     return

            queryDynamicValue = ""
            #Selenium returns a dictionary
            resultSelenium = {}

            classification_object = QuestionClassificationSVM.SVMClassifier()
            import spacy
            nlp_loader = spacy.load(EN_MODEL_MD)
            doc = nlp_loader(u'' + str(input))
            # if classification_object.classify_question(doc)[0] is not 'HUM' or 'DESC' or 'ENTY':
            #     print("question classification: ", classification_object.classify_question(doc)[0])
            #     resultSelenium = {"Status": "Question Classification Failed"}
            #     return resultSelenium

            systemHealthFlag = False
            stanford_parser = TestConnectionCoreNLP()
            resultOfConstituentParse = stanford_parser.constituencyParser(input)
            print(resultOfConstituentParse.pretty_print())
            print(resultOfConstituentParse.leaves())
            similarityFlag = stanford_parser.similarity_levenshtein("Is the system health good?", input)
            if(similarityFlag == False):
                similarityFlag = stanford_parser.similarity_levenshtein("How is the system status?", input)
            matchedContext = nlpTask.findNNSubtree(resultOfConstituentParse)
            #adjective_finder = nlpTask.printSubtrees(resultOfConstituentParse, 'ADJP', 'JJ')
            adjective_finder = nlpTask.printSubtrees(resultOfConstituentParse,'NP', 'JJ')
            if (len(matchedContext) == 0):
                print("No noun change with adjective")
                adjective = ast.literal_eval(json.dumps(adjective_finder))
                print("changed adjective", adjective[0])
                matchedContext.append(adjective[0])
                print("changed noun", matchedContext[-1])

            matchedContext = ast.literal_eval(json.dumps(matchedContext))
            machineIndex = [i for i, item in enumerate(matchedContext) if re.search('.*machine', item)]
            sensorIndex = [i for i, item in enumerate(matchedContext) if re.search('.*sensor', item)]
            machineTest = re.compile(".*machine")
            averageTest = re.compile(".*average")
            minimumKeyword = re.compile(".*minimum")
            maximumKeyword = re.compile(".*maximum")
            #filter creates a list in python 2.7
            #and filter(averageTest.match, matchedContext) == None
            if filter(machineTest.match, matchedContext) and 'value' in matchedContext and len(filter(averageTest.match, matchedContext)) == 0:
                print("filter dynamic query")
                path = SPARQLGeneratorClass.add_path_to_IRI('demofactory')
                queryDynamicValue = """select * where
                               { service <kvin:> { <http://localhost:10080/""" + path + """/""" + matchedContext[machineIndex[0]] + """/""" + matchedContext[sensorIndex[0]] + """> <http://example.org/""" + matchedContext[0] + """> ?v . ?v <kvin:limit> 1 ;
                               <kvin:value> ?value}} """

                print("queryDynamicValue", queryDynamicValue)
                resultSelenium = SPARQLGeneratorClass.queryTestingSelenium(queryDynamicValue)
                print("resultSelenium", resultSelenium)

            # and 'average' in matchedContext)
            elif filter(averageTest.match, matchedContext) and filter(machineTest.match, matchedContext) or similarityFlag == True:
                print("filter average query")
                path = SPARQLGeneratorClass.add_path_to_IRI('demofactory')
                queryDynamicAverage = """SELECT (AVG(?value) AS ?avg)
                WHERE {
                service <kvin:> {  <http://localhost:10080/""" + path + """/""" + matchedContext[machineIndex[0]] + """/""" +  matchedContext[sensorIndex[0]] + """> <http://example.org/value> ?v . ?v <kvin:limit> 10000; <kvin:value> ?value} }"""

                print("queryDynamicAverage", queryDynamicAverage)
                resultSelenium = SPARQLGeneratorClass.queryTestingSelenium(queryDynamicAverage)
                print("resultSelenium", resultSelenium)
                print("resulst selenium average", resultSelenium.get('avg'))
                #similarity flag should be checked every time even if in elif
                #otherwise we might get an error like system in an error state
                if (resultSelenium.get('avg') > 4.0) and similarityFlag == True:
                    systemHealthFlag = True
                    resultSelenium = {"Status": "System is working"}
                elif similarityFlag == True:
                    resultSelenium = {"Status": "System in an error state"}

            elif filter(minimumKeyword.match, matchedContext) and filter(machineTest.match, matchedContext) or 'minimum' in matchedContext:
                path = SPARQLGeneratorClass.add_path_to_IRI('demofactory')

                #a question for minimum value
                queryDynamicMinimum = """SELECT (MIN(?value) AS ?min)
                WHERE {
                service <kvin:> {  <http://localhost:10080/""" + path + """/""" + matchedContext[machineIndex[0]] + """/""" +  matchedContext[sensorIndex[0]] + """> <http://example.org/value> ?v . ?v <kvin:limit> 10000; <kvin:value> ?value} }"""
                resultSelenium = SPARQLGeneratorClass.queryTestingSelenium(queryDynamicMinimum)
                print("resultSelenium", resultSelenium)

            elif filter(maximumKeyword.match, matchedContext) and filter(machineTest.match, matchedContext) or 'maximum' in matchedContext:
                path = SPARQLGeneratorClass.add_path_to_IRI('demofactory')
                #A question for maxumum value
                queryDynamicMaximum = """ SELECT (MAX(?value) AS ?max)
                                WHERE {
                                service <kvin:> {  <http://localhost:10080/""" + path + """/""" + matchedContext[machineIndex[0]] + """/""" +  matchedContext[sensorIndex[0]] + """> <http://example.org/value> ?v . ?v <kvin:limit> 10000; <kvin:value> ?value} }"""
                resultSelenium = SPARQLGeneratorClass.queryTestingSelenium(queryDynamicMaximum)
                print("resultSelenium", resultSelenium)

            else:
                logger.info("This situation will be considered for other parts of linked factory")
                print("This situation will be considered for other parts of linked factory")
        except Exception as ex:
            logger.exception("Dynamic query connection error")
        return (resultSelenium, resultOfConstituentParse, systemHealthFlag)

    """Method: generated_data_query method is used for fetching data from static semantic sources defined by linkedfactory or enilink"""
    # Arguments
    #     input_text: a question or keyword based search items for question answering system.
    # Output shape
    #     It will give us a results in dictionary format for static input

    @staticmethod
    def generated_data_query_OPC(input):
        try:
            stanford_parser = TestConnectionCoreNLP()
            #The following is a tuple assignment
            #noun, verb = []
            noun = verb = []
            result_of_local_source = {}
            constituent_parse = stanford_parser.constituencyParser(input)
            print(constituent_parse.pretty_print())
            print(constituent_parse.leaves())
            #matchedContext = nlpTask.findNNSubtree(constituent_parse)
            parent_node_test = re.compile(".*parentnodeid")
            node_id_test = re.compile(".*nodeid")
            datablock_test = re.compile(".*datablock")
            station_test = re.compile(".*station")
            reference_test = re.compile(".*reference")

            # questionAnswering = QuestionClassifier.QuestionAssigner.predictQuestion(text_input)
            # if questionAnswering is 'unknown' or questionAnswering is 'who':
            #     return

            classification_object = QuestionClassificationSVM.SVMClassifier()
            import spacy
            nlp_loader = spacy.load(EN_MODEL_MD)
            doc = nlp_loader(u'' + str(input))
            question_classification = classification_object.classify_question(doc)[0]
            if question_classification != 'HUM' and question_classification != 'DESC' and question_classification != 'ENTY':
                resultSelenium = {"Status": "Question Classification Failed"}
                return resultSelenium

            prefix_query = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                                             PREFIX : <http://opcfoundation.org/UA/2011/03/UANodeSet.xsd#> 
                                             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                             PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                             PREFIX lf: <http://linkedfactory.org/vocab/> 
                                             PREFIX lf-plc: <http://linkedfactory.org/vocab/plc/> 
                                            """

            verb = nlpTask.spacyArchMatching(input)
            if (verb != None):
                print("type of verb", type(verb))
                print("type of processed verb", type(str(verb[0])))
                lemmatized_verb = stanford_parser.spacy_verb_lemmatizer(str(verb[0]))
                print("lemmatized verb", lemmatized_verb)
                print("type of lemmatized verb: ", type(lemmatized_verb))
                wordnetLatentAnalysis = nlpTask.wordnetLatentAnalysis(str(lemmatized_verb[0]), 'browse')

            noun = nlpTask.findNNSubtree(constituent_parse)
            matchedContext = ast.literal_eval(json.dumps(noun))
            print("noun", noun)

            #matched_verb = ast.literal_eval(json.dumps(verb[0]))
            # similarity_flag = False
            # similarity_flag = stanford_parser.similarity_jaro_winkler("Can you browse for me on generated data?", input)

            if (str(verb[0]).find('browse') != -1) and wordnetLatentAnalysis == True:

                browse_name_query = prefix_query + """ SELECT DISTINCT ?object
                                        WHERE {
                                        ?s :BrowseName ?object . 
                                        } """

                endpointRemote = SPARQLEndpoint("localhost", browse_name_query, "ttl", filename="SemanticSource/OPCGeneratedData.ttl")
                time.sleep(3)
                result_of_local_source = endpointRemote.sparqlQueryForLocalSource()
                # else:
                #     result_of_local_source = {"Status": "Query Wordnet Analysis is not correct"}

            if ('node' and 'id' in noun) or filter(node_id_test.match, matchedContext):
                node_id_query = prefix_query + """ SELECT DISTINCT ?object
                                WHERE {
                                  ?s :NodeId ?object .
                                   OPTIONAL { ?s :NodeId ?o. }
                                } 
                            """
                endpointRemote = SPARQLEndpoint("localhost", node_id_query, "ttl", filename="SemanticSource/OPCGeneratedData.ttl")
                time.sleep(3)
                result_of_local_source = endpointRemote.sparqlQueryForLocalSource()

            if ('parent' and 'node' and 'id') in noun or filter(parent_node_test.match, matchedContext):
                parent_node_id_query = prefix_query + """ SELECT DISTINCT ?object
                                WHERE {
                                  ?s :ParentNodeId ?object . }
                            """
                endpointRemote = SPARQLEndpoint("localhost", parent_node_id_query, "ttl", filename="SemanticSource/OPCGeneratedData.ttl")
                time.sleep(3)
                result_of_local_source = endpointRemote.sparqlQueryForLocalSource()

            if 'datablock' or 'data block' in noun or filter(datablock_test.match, matchedContext):
                query_data_block = prefix_query + """ SELECT DISTINCT ?object
                                WHERE {
                                  ?s lf-plc:dataBlock ?object . }
                            """
                endpointRemote = SPARQLEndpoint("localhost", query_data_block, "ttl", filename="SemanticSource/OPCGeneratedData.ttl")
                time.sleep(3)
                result_of_local_source = endpointRemote.sparqlQueryForLocalSource()

            if filter(station_test.match, matchedContext):
                """The following query might have changed with UNION"""
                query_station_identify = prefix_query +  """ SELECT DISTINCT *
                                WHERE { {SELECT ?object WHERE {
                                  ?s rdf:type ?o .
                                  ?s lf-plc:Station ?object . 
                                   } } UNION 
                                 { SELECT ?object
                                  WHERE {
                                  ?s rdf:type ?o .
                                  ?s lf-plc:CPU ?object . 
                                  
                                  } }
                                }
                            """
                endpointRemote = SPARQLEndpoint("localhost", query_station_identify, "ttl", filename="SemanticSource/OPCGeneratedData.ttl")
                time.sleep(3)
                result_of_local_source = endpointRemote.sparqlQueryForLocalSource()

            if filter(reference_test.match, matchedContext):
                """The following query is used for fetching references of nodes"""
                query_station_references = prefix_query + """ SELECT DISTINCT ?object 
                                WHERE {
                                  ?s :Reference ?object . } 
                            """
                endpointRemote = SPARQLEndpoint("localhost", query_station_references, "ttl",
                                                filename="SemanticSource/OPCGeneratedData.ttl")
                time.sleep(3)
                result_of_local_source = endpointRemote.sparqlQueryForLocalSource()
        except:
            print("An error happened while sending a result")


        return result_of_local_source



