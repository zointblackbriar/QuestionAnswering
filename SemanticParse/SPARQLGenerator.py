import SparqlEndpoint
from selenium import webdriver
from StanfordCoreNLP import ConnectionCoreNLP, TestConnectionCoreNLP
import re
import time

queryShowEverything = "SELECT * WHERE{ ?s ?p  ?o }"
queryCountAllRDF = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
sensorInfo = "sensor1"
machine1 = "machine"
queryDynamic = "select * where " \
               "{ service <kvin:> { <http://localhost:10080/linkedfactory/demofactory/machine1/sensor1> <http://example.org/value> ?v . ?v <kvin:limit> 1 ; " \
               "<kvin:time> ?time }}"

testQuery = "SELECT * { ?s ?factory:contains ?sensor5 } "

predefinedSelectQuery = """select * where {
                        service <kvin:> { <http://localhost:10080/linkedfactory/demofactory/machine1/sensor1> <http://example.org/value> ?v . ?v <kvin:limit> 1 ; <kvin:time> ?time }
                        }"""

obj = ConnectionCoreNLP()
def SPARQLGenerate(input):
    listOfPostTagger = obj.parse(input)
    #type list
    print("list of Post Tagger", listOfPostTagger)
    #matches = (x for x in listOfPostTagger  if x == 'NN')
    #print(matches)

def regexContains():
    textInput = "What is the current contains of sensor 1 of machine 1?"
    matchObj = re.match("^.(\bcontains\b)?.$", textInput)
    if matchObj:
        print("match")
    else:
        print("No match")
regexContains()

def testSPARQLGenerate():
    SPARQLGenerate("What is the current value of sensor 1 of machine 1?")

#testSPARQLGenerate()

def sampleTestChromeDriver():
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

def queryTestingSelenium():

    options = webdriver.ChromeOptions()
    #headless is a chromium option for silenty working
    options.add_argument("headless")
    driver = webdriver.Chrome('C:\\ProgramData\\chocolatey\\lib\\chromedriver\\tools\\chromedriver.exe', chrome_options=options)  # Optional argument, if not specified will search path.
    driver.get('http://localhost:10080/sparql')
    time.sleep(2)
    text_area = driver.find_element_by_id('query')
    text_area.send_keys(queryDynamic)
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

    driver.quit()
    print('Driver quit')

#queryTestingSelenium()


# obj = StanfordCoreNLP.TestPurpose()
# obj.runTest()



# endpointObjectHolder = SparqlEndpoint.SPARQLEndpoint("http://localhost:10080/sparql",
#                                                      queryShowEverything, "data/testFraunhoferData.ttl")
#
# print(endpointObjectHolder.sparqlQueryRemote())


