#!/usr/bin/env python
# coding: utf-8
from flask  import Flask, request, render_template, redirect, url_for, jsonify
#from flask_debugtoolbar import DebugToolbarExtension
import Utils
import QuepyTest
import nlquery
import logging
import threading
import time
import json
from SPARQLGenerator import  SPARQLGeneratorClass
import requests


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
# @app.before_first_request
# def activate_job():
#     def run_job():
#         while True:
#             print("Run recurring task")
#             time.sleep(3)
#
#     thread = threading.Thread(target=run_job)
#     thread.start()

@app.route('/')
def my_form():
    logging.warning("See this message in Flask Debug Toolbar!")
    return render_template('index.html')

@app.route('/integratedstaticmessage', methods=['GET', 'POST'])
def staticQuestion():
    try:
        queryResult = ""
        statement = [] #It should return as list
        queryLinkedFactory = request.get_data()
        queryLinkedFactory = Utils.questionMarkProcess(queryLinkedFactory)
        print("Posted data : {}".format(request.data))

        queryResult = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)[0]
        for stmt in queryResult:
            statement.append(stmt)
    except (RuntimeError, TypeError, NameError, Exception):
        app.logger.exception("Fraunhofer engine search error")
    #return ''+str(queryResult)
    """jsonify(result = statement)"""
    print("queryResult", queryResult)
    return jsonify(result = statement)

@app.route('/integrateddynamicmessage', methods=['GET', 'POST'])
def dynamicQuestion():
    try:
        #Todo you should turn connectNLP object into singleton
        dynamicQueryResult = {}
        queryLinkedFactory = request.get_data()
        """dynamicQueryResult, constituent_parser, health_flag"""
        dynamicQueryResult = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)[0]
    except (RuntimeError, TypeError, NameError, Exception):
        app.logger.exception("Fraunhofer engine search error")
    """jsonify(result=dynamicQueryResult)"""
    return jsonify(result=dynamicQueryResult)

def quepySender(quepyQuestion):
    handler_quepy = QuepyTest.QuepyMain()
    logging.warning("quepy!")
    global share_var_quepySender
    global share_var_sparql_queries
    quepy_test_result = None

    try:
        print_handlers = {
            "define": handler_quepy.print_define,
            "enum": handler_quepy.print_enum,
            "time": handler_quepy.print_time,
            "literal": handler_quepy.print_literal,
            "age": handler_quepy.print_age,
        }


        print (quepyQuestion)
        print ("-" * len(quepyQuestion))

        target, query, metadata =QuepyTest.dbpedia.get_query(quepyQuestion)
        time.sleep(4)

        if isinstance(metadata, tuple):
            query_type = metadata[0]
            metadata = metadata[1]
        else:
            query_type = metadata
            metadata = None

        if query is None:
            print("Query could not be generated \n")

        print("Query generated", query)
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
        #share_var_quepySender = results
        share_var_quepySender = "{0}".format(print_handlers[query_type](results, target, metadata))
        #share_var_quepySender = print_handlers
        #quepy_test_result = results['results']['bindings']
        quepy_test_result = "{0}".format(print_handlers[query_type](results, target, metadata))
        print("share_var_quepySender", type(share_var_quepySender))
        #print
        # share_var_quepySender = outputPython
        #share_var_sparql_queries = results

    except Exception as ex:
        app.logger.error("Handler is not working correctly: ", str(ex))
    return quepy_test_result

@app.route('/quepy', methods=['GET', 'POST'])
def quepyForm():
    # If you want to give an argument please use as follow
    # t = Thread(target=quepySender, args=(url, data))
    param_Question = request.form['quepyEngine']
    quepySender(str(param_Question))
    #print('share_var_sparql_queries', share_var_sparql_queries)
    #tuple format
    #return  '{} {} {}'.format(firstname, lastname, cellphone)
    if share_var_sparql_queries:
        return render_template('quepy.html', queryResult = share_var_sparql_queries, answer = share_var_quepySender), 200
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
        print(outputText)
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
        systemHealth = False
        resultOfConstituentParse = ""
        if request.form['fraunhoferEngine'] == None:
            return redirect('/', code=302)
        queryLinkedFactory = Utils.questionMarkProcess(request.form['fraunhoferEngine'])
        queryLinkedFactory = queryLinkedFactory.lower()

        #To control the value of checkbox if selected
        if bool(request.form.getlist('dynamicQuery')) == True:
            print("Dynamic Query")
            # Test the following line
            #questionAnswering = QuestionClassification.QuestionClassifier.QuestionAssigner.predictQuestion(queryLinkedFactory)
            #dynamicQueryResult, resultOfConstituentParse, systemHealth = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
            list_answer = SPARQLGeneratorClass.dynamic_query_triples(queryLinkedFactory)
            return render_template('fraunhoferengine.html', linkedFactoryQueryResult=list_answer[1], dynamicResult = list_answer[0])
        elif bool(request.form.getlist('generatedOPCQuery')) == True:
            list_answer = SPARQLGeneratorClass.generated_data_query_OPC(queryLinkedFactory)
            return render_template('fraunhoferengine.html', linkedFactoryQueryResult=list_answer[1], dynamicResult = list_answer[0])
        else:
            list_answer = SPARQLGeneratorClass.static_query_triples(queryLinkedFactory)
            print('sparqlQuery', list_answer[0])
            return render_template('fraunhoferengine.html', linkedFactoryQueryResult=list_answer[1], linkedFactorySparqlQuery = list_answer[0], dynamicResult = {})
    except (RuntimeError, TypeError, NameError, Exception):
        app.logger.exception("Fraunhofer engine search error")

    return redirect('/', code=302)

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()



if __name__ == '__main__':
    #app.jinja_env.cache = {}
    #start_runner()
    app.run(debug = True, host='0.0.0.0', port=8999, threaded=True)
    # Alternately
    # app.run(processes=3)



