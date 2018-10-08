import csv
from ValidURI import to_iri
from csv import DictReader
from rdflib import Dataset, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CSV2RDF():
    def __init__(self, filename):
        self._filename = filename


    def csvReader(self):
        try :
            with open (self._filename, 'r') as csvfile:
                #Set the right quote character and delimiter
                csvReader = csv.reader(csvfile, quotechar='"', delimiter=" ")
                logger.info("csvReader opened")

                #If the first row contains header information, fetch it like following
                header = next(csvReader)
                print ("Header", header)
                logger.info("Header info ok")

                print("Lines")
                rows = 0
                for line in csvReader:
                    """print(line)"""
                    rows = rows + 1
                logger.info("Lines info ok")

                return (rows,line)
        except:
            logger.error("There is an error while opening a csv file")

    def readFromMemory(self):
        #format is not correct
        try:
            with open(self._filename, 'r') as csvfile:
                text = [{k: v for k, v in row.items()}
                for row in csv.DictReader(csvfile, quotechar='"', delimiter=" ")]

            return text
        except:
            logger.error("There is an error while opening a file")

    def convertRDF(self):
        try:
            #Dataset is the object in which we will store our RDF graphs
            #URIRef is the datatype for URI-resources
            #Literal is the datatype for literal resources (string, dates etc.)
            #Namespace is used to create namespaces (parts of the URI's we are going to make
            #RDF, RDFS, OWL, and XSD are built in namespaces
            vocab = 'http://linkedfactory.iwu.fraunhofer.de/linkedfactory/demofactory'
            VOCAB = Namespace(vocab)
            csvContents = self.readFromMemory()
            data = "http://linkedfactory.iwu.fraunhofer.de/"
            DATA = Namespace(data)
            print(DATA)
            print(VOCAB)
            graphUri = URIRef("http://linkedfactory.iwu.fraunhofer.de/linkedfactory")
            dataset=Dataset()
            dataset.bind('linkedfactory', DATA)
            graph=dataset.graph(graphUri)
            print("Graph result is: ", graph)
            #A straighforward conversion
            #Make sure you have Literal objects for all literal values you need. Be sure to use the proper datatype or a language tag
            #Decide on what URI will be the 'primary key' for each now
            #Decide on the terms you are going to use to create the relations (predicates, properties)
            #Add the triples to the graph
            counterOfPages = self.csvReader()
            i = 0
            holder = self.csvReader()[0]
            for i in range(holder - 1):
                timeValues = self.csvReader()[1][i]

            print(timeValues)


            # for row in csvContents:
            #     time = URIRef(to_iri(data + row['time,value']))
            #     value = URIRef(to_iri(data + row['value']))
            #
            #     # All set... we are now going to add the triples to our graph
            #     graph.add((time, VOCAB['time'], value))
            #     graph.add((time, VOCAB['value'], time))


            print(dataset.serialize(format='trig'))
        except:
            logger.error("Something wrong when parsing")



obj = CSV2RDF("values.csv")
#obj.csvReader()
#print(obj.readFromMemory())
obj.convertRDF()