# coding: utf-8
import nltk
from flask  import Flask, request, render_template, redirect, url_for
#from flask_debugtoolbar import DebugToolbarExtension
import Utils
import QuepyTest
import nlquery
import logging
from threading import Thread
import time
import pdb
import json

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

@app.route('/parseData', methods=['GET', 'POST'])
def my_form_post():
    logging.warning("parseData!")
    text = request.form['question']
    processed_text = text.lower()
    print(processed_text)
    try:
        takeWords = []
        takeWords = Utils.clearTokenAndStopWords(processed_text)
        print(takeWords)
        tagged_Words = nltk.pos_tag(takeWords)
        print(tagged_Words)
        print("Searching...")
        Utils.taggedWhoQuestion(tagged_Words)
        #Utils.taggedWhereQuestion(tagged_Words)
        #Utils.taggedWhatQuestion(tagged_Words)
    except:
        print("An Exception caught")
    return redirect(url_for('index'))

def quepySender(quepyQuestion):
    logging.warning("quepy!")
    global share_var_quepySender
    global share_var_sparql_queries
    try:
            # The following question can be asked against DBpedia open domain resource
            # "Who is Fraunhofer ?",
            # "Who is Angela Merkel?",
            # "What is the language of Argentina?",
            # "what language is spoken in Argentina?",
            # "What is the population of China?",
            # "What is a car?",
            # "Who is Tom Cruise?",
            # "Who is George Lucas?",
            # "Who is Mirtha Legrand?",
            # "Name Fiat cars",
            # "time in argentina",
            # "what time is it in Chile?",
            # "List movies directed by Martin Scorsese",
            # "How long is Pulp Fiction",
            # "which movies did Mel Gibson starred?",
            # "When was Gladiator released?",
            # "who directed Pocahontas?",
            # "actors of Fight Club",
            # "How many people live in China?",
            # "What is the capital of Bolivia?",
            # "Who is the president of Argentina?"

        print_handlers = {
            "define": QuepyTest.print_define,
            "enum": QuepyTest.print_enum,
            "time": QuepyTest.print_time,
            "literal": QuepyTest.print_literal,
            "age": QuepyTest.print_age,
        }
        # outputPython = questions

        # for question in questions:

        print quepyQuestion
        print "-" * len(quepyQuestion)

        target, query, metadata =QuepyTest.dbpedia.get_query(quepyQuestion)
        #time.sleep(3)

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
    # pdb.set_trace()
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
    engine = nlquery.NLQueryEngine('localhost', 9000)

    try:
        app.logger.warning("Query Engine: %s", engine)
        print("engine", engine)

        textNL = request.form['nlqueryengine']
        textNL = textNL.encode('utf-8')
        print(textNL)
        #line = line.lower()
        #app.logger.info("Show the query: %s", line)
        outputText = engine.query(textNL, format_='plain')
        app.logger.info("Output the query: %s", outputText)
        share_var_nlQueryHandler = outputText
        print outputText
        if share_var_nlQueryHandler:
            return render_template('nlqueryengine.html', queryResultNLQuery=share_var_nlQueryHandler)

    except(RuntimeError, TypeError, NameError, Exception):
        app.logger.error("Handler is not working correctly: ", exc_info=True)


    return redirect('/', code=302)

if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0", port=8999)


