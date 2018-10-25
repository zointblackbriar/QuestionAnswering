#!/usr/bin/env python
# coding: utf-8
import nltk
from flask  import Flask, request, render_template, redirect, url_for
#from flask_debugtoolbar import DebugToolbarExtension
import Utils
import QuepyTest
import nlquery
import os
import logging
from threading import Thread
import time
import pdb
import json
import StanfordCoreNLP
from SPARQLGenerator import  SPARQLGeneratorClass

app = Flask(__name__)
# app.debug = True
# app.config['SECRET_KEY'] = 'development key'
# toolbar = DebugToolbarExtension(app)
# toolbar.init_app(app)

share_var_quepySender = None
share_var_nlQueryHandler = None
share_var_sparql_queries = None


@app.route('/')
def my_form():
    logging.warning("See this message in Flask Debug Toolbar!")
    return render_template('index.html')

# @app.route('/testForOtherAlg', methods=['GET', 'POST'])
# def my_form_post():
#     logging.warning("parseData!")
#     text = request.form['question']
#     processed_text = text.lower()
#     print(processed_text)
#     try:
#         takeWords = []
#         takeWords = Utils.clearTokenAndStopWords(processed_text)
#         print(takeWords)
#         tagged_Words = nltk.pos_tag(takeWords)
#         print(tagged_Words)
#         print("Searching...")
#         Utils.taggedWhoQuestion(tagged_Words)
#         #Utils.taggedWhereQuestion(tagged_Words)
#         #Utils.taggedWhatQuestion(tagged_Words)
#     except:
#         print("An Exception caught")
#     return redirect(url_for('index'))

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

            share_var_quepySender = results["results"]["bindings"]

        print_handlers[query_type](results, target, metadata)
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
        obj = StanfordCoreNLP.TestConnectionCoreNLP()
        testLinkedFactory = Utils.questionMarkProcess(request.form['fraunhoferEngine'])
        #testLinkedFactory = Utils.questionMarkProcess(testLinkedFactory)
        resultOfConstituentParse = obj.runTest(testLinkedFactory)
        print(resultOfConstituentParse.pretty_print())
        print(resultOfConstituentParse.leaves())
        sparqlQuery = SPARQLGeneratorClass.getInputQuery(testLinkedFactory, resultOfConstituentParse)
        # for row in sparqlQuery:
        #     item = row
        print('sparqlQuery', sparqlQuery)
        return render_template('fraunhoferengine.html', linkedFactoryQueryResult=resultOfConstituentParse, linkedFactorySparqlQuery = sparqlQuery)

    except (RuntimeError, TypeError, NameError, Exception):
        app.logger.exception("Fraunhofer engine search error")

    return redirect('/', code=302)

#Angular JS App Test Purpose
@app.route('/question/query<string>')
def evaluateQuery():
    data = request.args.get('query')
    print(data)
    return 'hello world'


if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=8999)


