#!/usr/bin/env python
# coding: utf-8
import nltk
from flask  import Flask, request, render_template, redirect, url_for, jsonify
#from flask_debugtoolbar import DebugToolbarExtension
import Utils
import QuepyTest
import nlquery
import os
import logging
#from threading import Thread
import threading
import time
import pdb
import json
import StanfordCoreNLP
from SPARQLGenerator import  SPARQLGeneratorClass
import sys, os.path
import QuestionClassificiation



app = Flask(__name__)
app.logger.info('This is a log message')
# app.debug = True
# app.config['SECRET_KEY'] = 'development key'
# toolbar = DebugToolbarExtension(app)
# toolbar.init_app(app)

share_var_quepySender = None
share_var_nlQueryHandler = None
share_var_sparql_queries = None

#Added a thread pool support before requesting
#Daemon Threads
@app.before_first_request
def activate_job():
    def run_job():
        while True:
            #print("Run recurring task")
            time.sleep(1)

    thread = threading.Thread(target=run_job)
    thread.start()

@app.route('/')
def my_form():
    logging.warning("See this message in Flask Debug Toolbar!")
    return render_template('index.html')

@app.route('/testForWebService', methods=['GET', 'POST'])
def staticQuestion():
    try:
        queryResult = ""
        statement = [] #It should return as list
        connectNLP = StanfordCoreNLP.TestConnectionCoreNLP()
        queryLinkedFactory = request.data
        queryLinkedFactory = Utils.questionMarkProcess(queryLinkedFactory)
        print("Posted data : {}".format(request.data))
        resultOfConstituentParse = connectNLP.constituencyParser(queryLinkedFactory)
        print(resultOfConstituentParse)
        resultofDependencyParser = connectNLP.dependencyParser(queryLinkedFactory)
        print(resultofDependencyParser)

        queryResult = SPARQLGeneratorClass.getInputQuery(resultOfConstituentParse, resultofDependencyParser, param_posTagger=None)
        for stmt in queryResult:
            statement.append(stmt)
    except (RuntimeError, TypeError, NameError, Exception):
        app.logger.exception("Fraunhofer engine search error")
    #return ''+str(queryResult)
    return jsonify(result = statement)

@app.route('/testForDynamicQuestion', methods=['GET', 'POST'])
def dynamicQuestion():
    try:
        #Todo you should turn connectNLP object into singleton
        dynamicQueryResult = {}
        connectNLP = StanfordCoreNLP.TestConnectionCoreNLP()
        queryLinkedFactory = request.data
        resultOfConstituentParse = connectNLP.constituencyParser(queryLinkedFactory)
        print(resultOfConstituentParse.pretty_print())
        print(resultOfConstituentParse.leaves())
        resultofDependencyParser = connectNLP.dependencyParser(queryLinkedFactory)
        print(resultofDependencyParser)
        dynamicQueryResult = SPARQLGeneratorClass.getDynamicQuery(queryLinkedFactory, resultOfConstituentParse)
    except (RuntimeError, TypeError, NameError, Exception):
        app.logger.exception("Fraunhofer engine search error")
    return jsonify(result=dynamicQueryResult)

def quepySender(quepyQuestion):
    logging.warning("quepy!")
    global share_var_quepySender
    global share_var_sparql_queries
    try:
        print_handlers = {
            "define": QuepyTest.print_define,
            "enum": QuepyTest.print_enum,
            "time": QuepyTest.print_time,
            "literal": QuepyTest.print_literal,
            "age": QuepyTest.print_age,
        }


        print quepyQuestion
        print "-" * len(quepyQuestion)

        target, query, metadata =QuepyTest.dbpedia.get_query(quepyQuestion)
        time.sleep(4)

        if isinstance(metadata, tuple):
            query_type = metadata[0]
            metadata = metadata[1]
        else:
            query_type = metadata
            metadata = None

        if query is None:
            print "Query could not be generated \n"

        print query
        share_var_sparql_queries = query

        if target.startswith("?"):
            target = target[1:]
        if query:
            QuepyTest.sparql.setQuery(query)
            QuepyTest.sparql.setReturnFormat(QuepyTest.JSON)
            results = QuepyTest.sparql.query().convert()
            with open('data.json', 'w+') as outfile:
                json.dump(results["results"]["bindings"], outfile)

            if not results["results"]["bindings"]:
                share_var_quepySender = "No answer from wikidata"


        #print_handlers[query_type](results, target, metadata)
        share_var_quepySender = results
        #share_var_quepySender = "{0}".format(print_handlers[query_type](results, target, metadata))
        #print
        # share_var_quepySender = outputPython
        #share_var_sparql_queries = results

    except Exception as ex:
        app.logger.error("Handler is not working correctly: ", str(ex))

@app.route('/quepy', methods=['GET', 'POST'])
def quepyForm():
    # If you want to give an argument please use as follow
    # t = Thread(target=quepySender, args=(url, data))
    param_Question = request.form['quepyEngine']
    quepySender(param_Question)
    #print('share_var_sparql_queries', share_var_sparql_queries)
    #tuple format
    #return  '{} {} {}'.format(firstname, lastname, cellphone)
    if share_var_sparql_queries:
        return render_template('quepy.html', queryResult = share_var_sparql_queries, answer = share_var_quepySender)

    return redirect('/', code=302)


@app.route('/nlqueryengine', methods=['GET', 'POST'])
def nlQueryEngine():

    logging.warning("nlQueryEngine!")
    global share_var_nlQueryHandler
    outputText = ""
    try:
        engine = nlquery.NLQueryEngine('localhost', 9000)
        app.logger.warning("Query Engine: %s", engine)
        textNL = request.form['nlqueryengine']
        textNL = textNL.encode('utf-8')
        print(textNL)
        outputText = engine.query(textNL, format_='plain')
        time.sleep(2)
        app.logger.info("Output the query: %s", outputText)
        share_var_nlQueryHandler = outputText
        print outputText
        if share_var_nlQueryHandler:
            return render_template('nlqueryengine.html', queryResultNLQuery=share_var_nlQueryHandler)

    except(RuntimeError, TypeError, NameError, Exception):
        if 'CoreNLP Server' in str(Exception):
            app.logger.error(500, message='Cannot connect to CoreNLP server')
        else:
            app.logger.error("Handler is not working correctly: ", exc_info=True)


    return redirect('/', code=302)

@app.route('/fraunhoferengine', methods=['GET', 'POST'])
def LinkedFactoryQuery():
    try:
        #dynamicQueryResult = {}
        resultOfConstituentParse = ""
        #for checkbox
        obj = StanfordCoreNLP.TestConnectionCoreNLP()
        if request.form['fraunhoferEngine'] == None:
            return redirect('/', code=302)
        queryLinkedFactory = Utils.questionMarkProcess(request.form['fraunhoferEngine'])
        resultOfConstituentParse = obj.constituencyParser(queryLinkedFactory)
        print(resultOfConstituentParse.pretty_print())
        print(resultOfConstituentParse.leaves())
        resultofDependencyParser = obj.dependencyParser(queryLinkedFactory)
        resultofPosTagger = obj.posTaggerSender(queryLinkedFactory)
        print(resultofDependencyParser)
        #To control the value of checkbox if selected
        if bool(request.form.getlist('dynamicQuery')) == True:
            print("Dynamic Query")
            # Test the following line
            questionAnswering = QuestionClassificiation.QuestionClassifier.QuestionAssigner.encoderPass(queryLinkedFactory)
            if questionAnswering == 'affirmation' or questionAnswering == 'what':
                dynamicQueryResult = SPARQLGeneratorClass.getDynamicQuery(queryLinkedFactory, resultOfConstituentParse)
                return render_template('fraunhoferengine.html', linkedFactoryQueryResult=resultOfConstituentParse, dynamicResult = dynamicQueryResult)
            else:
                return redirect('/', code=302)
        else:
            sparqlQuery = SPARQLGeneratorClass.getInputQuery(resultOfConstituentParse, resultofDependencyParser, resultofPosTagger)
            print('sparqlQuery', sparqlQuery)
            return render_template('fraunhoferengine.html', linkedFactoryQueryResult=resultOfConstituentParse, linkedFactorySparqlQuery = sparqlQuery, dynamicResult = {})
    except (RuntimeError, TypeError, NameError, Exception):
        app.logger.exception("Fraunhofer engine search error")

    return redirect('/', code=302)


if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=8999)


