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

    #sampleTestChromeDriver()
    #Test is succesful

    #We will use selenium tool to reach SPARQL Endpoint
    def queryTestingSelenium(self):
        queryDynamicTime = """select * where 
                       { service <kvin:> { <http://localhost:10080/linkedfactory/demofactory/machine1/sensor1> <http://example.org/value> ?v . ?v <kvin:limit> 1 ; 
                       <kvin:time> ?time }} """

        #question is : What is the value of sensor1 in machine1
        queryDynamicValue = """select * where 
                       { service <kvin:> { <http://localhost:10080/linkedfactory/demofactory/machine1/sensor1> <http://example.org/value> ?v . ?v <kvin:limit> 1 ; 
                       <kvin:value> ?value}} """

        queryDynamicAverage = """SELECT (AVG(?value) AS ?avg) 
       (MIN(?value) AS ?min) 
       (MAX(?value) AS ?max) 
WHERE { 

service <kvin:> {  <http://localhost:10080/linkedfactory/demofactory/machine1/sensor1> <http://example.org/value> ?v . ?v <kvin:limit> 10000; <kvin:value> ?value}
}"""

        options = webdriver.ChromeOptions()
        #headless is a chromium option for silenty working
        #options.add_argument("headless")
        driver = webdriver.Chrome('C:\\ProgramData\\chocolatey\\lib\\chromedriver\\tools\\chromedriver.exe', chrome_options=options)  # Optional argument, if not specified will search path.
        driver.get('http://localhost:10080/sparql')
        time.sleep(2)
        text_area = driver.find_element_by_id('query')
        select = Select(driver.find_element_by_id('model'))
        select.select_by_visible_text('<http://linkedfactory.iwu.fraunhofer.de/data/>')
        #or you can change with the following case
        # <enilink:model:users>
        #select = Select(driver.find_element_by_name('<enilink:model:users>'))
        text_area.send_keys(queryDynamicAverage)
        driver.find_element_by_id('#submitBtn').click()
        time.sleep(1)
        print('Result is printed out')
        table = driver.find_element_by_css_selector(".table.table-hover")
        head = driver.find_element_by_tag_name('thead')
        body=driver.find_element_by_tag_name('tbody')
        elements = []
        head_line = head.find_element_by_tag_name("tr")
        elements = [header.text.encode("utf8") for header in head_line.find_elements_by_tag_name('td')]
        elements.append(",".join(elements))
        print(elements)

        #driver.quit()
        print('Driver quit')

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
    def getInputQuery(param_inputFromFlask, param_ConstituencyParser):

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
        sparqlQuery = """select * where {
                            service <kvin:> { <http://localhost:10080/linkedfactory/demofactory/machine1/sensor1> <http://example.org/value> ?v . ?v <kvin:limit> 1 ; <kvin:time> ?time }
                            }"""

        #tree = nlpTask.runTest(param_inputFromFlask)

        logger.info("check wordnet synonym analysis")
        #wordnet synonym analysis
        try:
            if nlpTask.simulation(verb[0], 'contains') == True:
                logger.info("here we inside of if true")

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
                    print("To do with give sentences")
                    parameterizedQuery = parameterizedQuery + SPARQLGeneratorClass.selectQueryLevel(noun[0]) + """>""" + """ factory:contains ?o . }"""
                    endpointRemote = SPARQLEndpoint("localhost", parameterizedQuery, "ttl",
                                                    filename="DataSource/FraunhoferData.ttl")
                    resultOFLocalSource = endpointRemote.sparqlQueryForLocalSource()
                    # All of them are test codes
                    # queryTestingSelenium()
        except (Exception):
            logger.exception("parameterized Query has some errors")
        return resultOFLocalSource


obj = SPARQLGeneratorClass()
#Test succesful
#obj.sampleTestChromeDriver()
obj.queryTestingSelenium()