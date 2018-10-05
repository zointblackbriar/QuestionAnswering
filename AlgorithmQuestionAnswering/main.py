# coding: utf-8
import nltk
from flask  import Flask, request, render_template, redirect, url_for
import Utils
import QuepyTest
import nlquery


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def my_form():
    return render_template('sender.html')

@app.route('/parseData', methods=['GET', 'POST'])
def my_form_post():
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

@app.route('/quepy', methods=['GET', 'POST'])
def quepyForm():
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
        #return redirect(url_for('index'))
        return 'result is ok'
    except(RuntimeError, TypeError, NameError):
        pass


@app.route('/nlqueryengine', methods=['GET', 'POST'])
def quepyForm():
    engine = nlquery.NLQueryEngine('localhost', 9000)
    try:
        line = request.form['nlquery']
        line = line.lower()
        print engine.query(line, format_='plain')
    except(RuntimeError, TypeError, NameError):
        pass
    #return redirect(url_for('/'))
    return 'result is ok'

if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0", port=8999)


