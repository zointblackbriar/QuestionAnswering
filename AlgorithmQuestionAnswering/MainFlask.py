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

app = Flask(__name__)
# app.debug = True
# app.config['SECRET_KEY'] = 'development key'
# toolbar = DebugToolbarExtension(app)
# toolbar.init_app(app)

share_var_quepySender = None
share_var_nlQueryHandler = None


@app.route('/')
def my_form():
    logging.warning("See this message in Flask Debug Toolbar!")
    return render_template('sender.html')

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

def quepySender():
    logging.warning("quepy!")
    global share_var_quepySender
    try:
        default_questions = [
            "Where is Fraunhofer ?",
            "Who is Angela Merkel?",
            "When Angela Merkel born?",
            # "Name Volkswagen cars",
            # "time in Turkey",
            # "What time is it in Ankara?",
            # "List movies directed by Quantin Tarantino",
            # "How long is Kill Bill 2",
            # "which movies did Mel Gibson starred?",
            # "When was Gladiator released?",
            # "actors of Fight Club",
            "What is the language of Argentina?",
            "what language is spoken in Argentina?",
            "What is the population of China?",
            "What is a car?",
            "Who is Tom Cruise?",
            "Who is George Lucas?",
            "Who is Mirtha Legrand?",
            # "List Microsoft software",
            "Name Fiat cars",
            "time in argentina",
            "what time is it in Chile?",
            "List movies directed by Martin Scorsese",
            "How long is Pulp Fiction",
            "which movies did Mel Gibson starred?",
            "When was Gladiator released?",
            "who directed Pocahontas?",
            "actors of Fight Club",
            # "How many people live in China?",
            # "What is the capital of Bolivia?",
            # "Who is the president of Argentina?"
        ]
        questions = default_questions

        print_handlers = {
            "define": QuepyTest.print_define,
            "enum": QuepyTest.print_enum,
            "time": QuepyTest.print_time,
            "literal": QuepyTest.print_literal,
            "age": QuepyTest.print_age,
        }
        outputPython = questions

        for question in questions:
            print question
            print "-" * len(question)

            target, query, metadata =QuepyTest.dbpedia.get_query(question)

            if isinstance(metadata, tuple):
                print 'Hello metadata'
                query_type = metadata[0]
                metadata = metadata[1]
            else:
                print 'Hello quepy type'
                query_type = metadata
                metadata = None

            if query is None:
                print "Query not generated :(\n"
                continue

            print query

            if target.startswith("?"):
                target = target[1:]
            if query:
                QuepyTest.sparql.setQuery(query)
                QuepyTest.sparql.setReturnFormat(QuepyTest.JSON)
                results = QuepyTest.sparql.query().convert()

                if not results["results"]["bindings"]:
                    print "No answer found :("
                    continue

            print_handlers[query_type](results, target, metadata)
            print
            print("Output Python", outputPython)
            share_var_quepySender = outputPython
    except Exception as ex:
        app.logger.error("Handler is not working correctly: ", str(ex))

@app.route('/quepy', methods=['GET', 'POST'])
def quepyForm():
    # If you want to give an argument please use as follow
    # t = Thread(target=quepySender, args=(url, data))

    t = Thread(target=quepySender)
    t.daemon = True
    t.start()
    time.sleep(3)
    if share_var_quepySender:
        return render_template('quepy.html', output = str(share_var_quepySender))

    return redirect('/', code=302)

def nlQueryHandler():
    logging.warning("nlQueryEngine!")
    global share_var_nlQueryHandler
    outputText = ""
    try:
        engine = nlquery.NLQueryEngine('localhost', 9000)
        time.sleep(3)
        app.logger.warning("Query Engine: %s", engine)
        print("engine", engine)
        line = request.form['nlquery']
        print(line)
        line = line.lower()
        app.logger.info("Show the query: %s", line)
        print("line", line)
        outputText = engine.query(line, format_='plain')
        app.logger.info("Output the query: %s", outputText)
        share_var_nlQueryHandler = outputText
        print outputText

    except(RuntimeError, TypeError, NameError, Exception):
        app.logger.error("Handler is not working correctly: ", exc_info=True)

@app.route('/nlqueryengine', methods=['GET', 'POST'])
def nlQueryEngine():
    t = Thread(target=nlQueryHandler)
    t.daemon = True
    t.start()
    if share_var_nlQueryHandler:
        return render_template('nlqueryengine.html', output = str(share_var_nlQueryHandler))

    return redirect('/', code=302)

if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0", port=8999)


