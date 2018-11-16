#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from StanfordCoreNLP import ConnectionCoreNLP, TestConnectionCoreNLP
from SparqlEndpoint import SPARQLEndpoint
import re
import time
import logging
import json, ast

logging.info('Starting logger for ...') #or call logging.basicConfig
# Set log name
logger = logging.getLogger(__name__)


obj = ConnectionCoreNLP()
nlpTask = TestConnectionCoreNLP()


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
    #Switch case
    def selectQueryLevel(item):
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
            "Aximus": """linkedfactory/IWU/E3-Sim/FoFab/Aximus""",
            "BDM2000": """linkedfactory/IWU/E3-Sim/FoFab/BDM2000""",
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

        #print(result)

    @staticmethod
    def getInputQuery(param_ConstituencyParser, param_DependencyParser, param_posTagger):
        verb = []
        noun = []
        #verb = nlpTask.printSubtrees(param_ConstituencyParser, 'VP', 'VBZ')
        verb = nlpTask.findVPSubtree(param_ConstituencyParser)[0]
        noun = nlpTask.printSubtrees(param_ConstituencyParser, 'NN', 'NNP')
        #noun = nlpTask.findNNSubtree(param_ConstituencyParser)[0]
        verb = ast.literal_eval(json.dumps(verb))
        noun = ast.literal_eval(json.dumps(noun))
        print("verb", verb)
        print("noun", noun[len(noun)-1])
        normalQueryDependency = [(u'ROOT', 0, 4), (u'punct', 4, 1), (u'det', 3, 2), (u'nsubj', 4, 3), (u'punct', 4, 5), (u'punct', 4, 6), (u'ROOT', 0, 1)]
        #inversedQueryDependency = [(u'ROOT', 0, 3), (u'det', 2, 1), (u'nsubj', 3, 2), (u'punct', 3, 4)]
        inversedQueryDependency = [(u'ROOT', 0, 2), (u'nsubj', 2, 1), (u'dobj', 2, 3), (u'punct', 2, 4), (u'ROOT', 0, 1)]
        #param_DependencyParser == [(u'ROOT', 0, 2), (u'nsubj', 2, 1), (u'dobj', 2, 3), (u'punct', 2, 4)] or
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

        logger.info("check wordnet synonym analysis")
        #wordnet synonym analysis
        try:
            #get a verb which has been analyzed and compare with its dependency parse tree against inverse query
            if (nlpTask.wordnetLatentAnalysis(verb[0], 'contains') == True) and (param_DependencyParser == normalQueryDependency):
                logger.info("Contains verb analyzed")
                print("Parameterized Query")
                parameterizedQuery = parameterizedQuery + str(SPARQLGeneratorClass.selectQueryLevel(noun[len(noun)-1])) + """>""" + """ factory:contains ?o . }"""
                print('parameterizedQuery', parameterizedQuery)
                endpointRemote = SPARQLEndpoint("localhost", parameterizedQuery, "ttl", filename="DataSource/FraunhoferData.ttl")
                time.sleep(3)
                resultOFLocalSource = endpointRemote.sparqlQueryForLocalSource()

            #The following query has a bug which its first line of condition
            # elif ([(u'contains', u'VBZ')] == [s for s in param_posTagger if 'VBZ' in s]) and \
            #         (param_DependencyParser == [(u'ROOT', 0, 2), (u'nsubj', 2, 1), (u'dobj', 2, 3), (u'punct', 2, 4)]) and \
            #             nlpTask.wordnetLatentAnalysis(ast.literal_eval(json.dumps(nlpTask.findVPSubtree(param_ConstituencyParser)[0])), "contains"):
            elif ( param_DependencyParser == inversedQueryDependency) and \
                    nlpTask.wordnetLatentAnalysis(ast.literal_eval(json.dumps(nlpTask.findVPSubtree(param_ConstituencyParser)[0])), "contains"):

                print("Inversed Query")
                inversedQuery = prefixEdit + """ SELECT ?s ?o WHERE { ?s  factory:contains """
                inversedQuery = inversedQuery + """<http://linkedfactory.iwu.fraunhofer.de/""" + str(SPARQLGeneratorClass.selectQueryLevel(noun[len(noun)-1])) + """>. }"""
                print("inversedQuery", inversedQuery)
                endpointRemote = SPARQLEndpoint("localhost", inversedQuery, "ttl", filename="DataSource/FraunhoferData.ttl")
                time.sleep(3)
                resultOFLocalSource = endpointRemote.sparqlQueryForLocalSource()
            else:
                #noun = ast.literal_eval(json.dumps(noun))
                print("No specific verb")
                if noun[len(noun)-1] != None:
                    #Give me all of members linkedfactory? == linkedfactory - nn
                    parameterizedQuery = parameterizedQuery + str(SPARQLGeneratorClass.selectQueryLevel(noun[len(noun)-1])) + """>""" + """ factory:contains ?o . }"""
                    endpointRemote = SPARQLEndpoint("localhost", parameterizedQuery, "ttl",
                                                    filename="DataSource/FraunhoferData.ttl")
                    resultOFLocalSource = endpointRemote.sparqlQueryForLocalSource()
        except (Exception):
            logger.exception("parameterized Query has some errors")
        return resultOFLocalSource

    @staticmethod
    def getDynamicQuery(input, parsedTree):
        try:
            queryDynamicValue = ""
            #Selenium returns a dictionary
            resultSelenium = {}
            #pattern = '^[a-zA-Z]+\s+\d+\s+[\d\:]+'
            matchedContext = nlpTask.findNNSubtree(parsedTree)
            #adjectiveFinder = nlpTask.printSubtrees(parsedTree, "JJ", "")
            matchedContext = ast.literal_eval(json.dumps(matchedContext))
            machineIndex = [i for i, item in enumerate(matchedContext) if re.search('.*machine', item)]
            sensorIndex = [i for i, item in enumerate(matchedContext) if re.search('.*sensor', item)]
            machineTest = re.compile(".*machine")
            averageTest = re.compile(".*average")
            #re.findall(pattern, "machine")
            if filter(machineTest.match, matchedContext) and 'value' in matchedContext:
                print("filter dynamic query")
                path = SPARQLGeneratorClass.selectQueryLevel('demofactory')
                queryDynamicValue = """select * where
                               { service <kvin:> { <http://localhost:10080/""" + path + """/""" + matchedContext[machineIndex[0]] + """/""" + matchedContext[sensorIndex[0]] + """> <http://example.org/""" + matchedContext[0] + """> ?v . ?v <kvin:limit> 1 ;
                               <kvin:value> ?value}} """

                print("queryDynamicValue", queryDynamicValue)
                resultSelenium = SPARQLGeneratorClass.queryTestingSelenium(queryDynamicValue)
                print("resultSelenium", resultSelenium)


            elif filter(averageTest.match, matchedContext) and filter(machineTest.match, matchedContext):
                print("filter average query")
                path = SPARQLGeneratorClass.selectQueryLevel('demofactory')
                queryDynamicAverage = """SELECT (AVG(?value) AS ?avg)
                       (MIN(?value) AS ?min)
                       (MAX(?value) AS ?max)
                WHERE {

                service <kvin:> {  <http://localhost:10080/""" + path + """/""" + matchedContext[machineIndex[0]] + """/""" +  matchedContext[sensorIndex[0]] + """> <http://example.org/value> ?v . ?v <kvin:limit> 10000; <kvin:value> ?value} }"""

                print("queryDynamicAverage", queryDynamicAverage)
                resultSelenium = SPARQLGeneratorClass.queryTestingSelenium(queryDynamicAverage)
                print("resultSelenium", resultSelenium)
            else:
                logger.info("This situation will be considered for other parts of linked factory")
        except Exception as ex:
            logger.exception("Dynamic query connection error")
        return resultSelenium

