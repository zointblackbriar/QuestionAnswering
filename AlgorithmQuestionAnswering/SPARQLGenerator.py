#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from StanfordCoreNLP import ConnectionCoreNLP, TestConnectionCoreNLP
from SparqlEndpoint import SPARQLEndpoint
import Utils
import re
import pdb
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
            "glt": """linkedfactory/IWU/FoFab/GLT""",
            "kälte": """linkedfactory/IWU/FoFab/GLT/Kälte""",
            "wärme": """linkedfactory/IWU/FoFab/Wärme""",
            "gmx": """linkedfactory/IWU/FoFab/GMX""",
            "nshv": """linkedfactory/IWU/FoFab/NSHV""",
            "versuchsfeld": """linkedfactory/IWU/FoFab/NSHV/Versuchsfeld""",
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

        }
        return switcher.get(item)

        #print(result)

    @staticmethod
    def getInputQuery(param_ConstituencyParser):

        verb = nlpTask.printSubtrees(param_ConstituencyParser, 'VP', None)
        noun = nlpTask.printSubtrees(param_ConstituencyParser, 'NN', 'NNP')
        verb = ast.literal_eval(json.dumps(verb))
        noun = ast.literal_eval(json.dumps(noun))
        print("verb", verb)
        print("noun", noun)
        parameterizedQuery = """PREFIX factory: <http://linkedfactory.iwu.fraunhofer.de/vocab#>
                                         PREFIX : <http://linkedfactory.iwu.fraunhofer.de/data/>
                                         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                         PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                         SELECT ?s ?o WHERE {
                                          <http://linkedfactory.iwu.fraunhofer.de/"""

        resultSparqlQuery = ""

        logger.info("check wordnet synonym analysis")
        #wordnet synonym analysis
        try:
            if nlpTask.simulation(verb[0], 'contains') == True:
                logger.info("Contains verb analyzed")
                parameterizedQuery = parameterizedQuery + SPARQLGeneratorClass.selectQueryLevel(noun[0]) + """>""" + """ factory:contains ?o . }"""
                print('parameterizedQuery', parameterizedQuery)
                endpointRemote = SPARQLEndpoint("localhost", parameterizedQuery, "ttl", filename="DataSource/FraunhoferData.ttl")
                time.sleep(3)
                resultOFLocalSource = endpointRemote.sparqlQueryForLocalSource()
            else:
                #noun = ast.literal_eval(json.dumps(noun))
                if noun[0] != None:
                    #noun = nlpTask.printSubtrees(param_ConstituencyParser, 'NNP')
                    #Give me all of members linkedfactory? == linkedfactory - nn
                    parameterizedQuery = parameterizedQuery + SPARQLGeneratorClass.selectQueryLevel(noun[0]) + """>""" + """ factory:contains ?o . }"""
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
            matchedContext = nlpTask.findSpecificSubtree(parsedTree)
            adjectiveFinder = nlpTask.printSubtrees(parsedTree, "JJ", "")
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


            elif filter(averageTest.match, adjectiveFinder) and filter(machineTest.match, matchedContext):
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

