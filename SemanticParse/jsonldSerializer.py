from rdflib import Graph, plugin
from rdflib.serializer import Serializer
from rdflib.plugin import register, Serializer, Parser
register('json-ld', Serializer, 'rdflib_jsonld.serializer', 'JsonLDSerializer')
import json

with open('data/e3fabrik.ttl', 'r') as outfile:
    outputText = outfile.read()

#print(outputText)

# testrdf = '''@prefix dc: <http://purl.org/dc/terms/> .
#             <http://example.org/about>
#                 dc:title "Someone's HomePage"@en .'''

g = Graph().parse(data=outputText, format='ttl')
outputJsonLD = g.serialize(format='json-ld', indent=4)

#print(g.serialize(format='json-ld', indent=4))

with open("data/e3fabrik.jsonld", "w+") as writeFile:
    writeFile.write(str(outputJsonLD))

print("File Handler closed")