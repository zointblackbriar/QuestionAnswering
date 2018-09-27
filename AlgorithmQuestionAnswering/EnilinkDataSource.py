from flask import Flask

app = Flask(__name__)

@app.route('http://linkedfactory.iwu.fraunhofer.de/linkedfactory/**')
def jsonDataFetcher():
    
    return "something else from enilink source"