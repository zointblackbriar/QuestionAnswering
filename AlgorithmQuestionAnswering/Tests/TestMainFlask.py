#!/usr/bin/env python
# coding: utf-8

import unittest
import os
os.chdir(r'../')

from MainFlask import app
from flask_testing import TestCase

htmlMainItem = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Sender Page</title>
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" href="../static/input.css" src="/static/input.css">
    <link rel="stylesheet" href="../static/button.css" src="/static/button.css">
    <link rel="stylesheet" href="../static/sender.css" src="/static/sender.css">

    <link href='https://fonts.googleapis.com/css?family=Pacifico' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

</head>

<body class="body">

    <div class="col-6">

        <div class="col-12">
            <a class="col-12" href="/" id="logo">Question Answering</a>
            <ul id="menu">
                <li><a href="https://www.iwu.fraunhofer.de/"><span>About the Company</span></a></li>
            </ul>
            <br>
            <br>
            <br>
            <!--<div class="wrapper"> -->
            <br>
            <br>
            <br>
            <br>
            <div class="col-md-6">
                <form method="POST" action="/nlqueryengine">
                    <p> Wikidata Question Engine:
                        <input type="text" name="nlqueryengine" id="nlqueryInput" class="Input-text" placeholder="Who is Angela Merkel?">
                    </p>
                    <label for="input" class="Input-label">Please ask a question</label>
                    <button class="action-button shadow animate blue" type="submit" name="wikidataEngine">Wikidata Question</button>
                </form>
            </div>
            <div class="col-md-6">
                <form method="POST" action="/quepy">
                    <p> Quepy Engine:
                        <input type="text" name="quepyEngine" id="quepyInput" class="Input-text" placeholder="Who is Fraunhofer?">
                    </p>
                    <label for="input" class="Input-label">Ask a question to quepy</label>
                    <button class="action-button shadow animate blue" type="submit" name="quepyEngine">Quepy</button>
                    <!-- href="/quepy" -->
                </form>
            </div>
            <div class="col-md-6">
                <form method="POST" action="/fraunhoferengine">
                    <p> Linked Factory Engine:
                        <input type="text" name="fraunhoferEngine" id="fraunInput" class="Input-text" placeholder="Give me all of members in linkedfactory?">
                    </p>
                    <label for="input" class="Input-label">Ask a question to Linked Factory</label>
                    <button class="action-button shadow animate blue" type="submit" name="fraunhoferEngine">Linked Factory</button>
                    <input type="checkbox" name="dynamicQuery" value="Dynamic_Query"><bold>ENILINK</bold>
                    </input>
                </form>
            </div>
            <br>
            <br>
        </div>
    </div>

</body>

</html>"""

class FlaskTesting(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        #creates a test client
        self.app = app.test_client()
        #propagate the exceptions to the test client
        self.app.testing = True

    #Executed before the tests
    def tearDown(self):
        pass

    def quepyRequest(self, sentence):
        return self.app.post('/quepy', data=sentence, follow_redirects = True)

    def nlqueryRequest(self, sentence):
        return self.app.post('nlqueryengine', data=sentence, follow_redirects=True)

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_quepy_module(self):
        #result = self.app.get('/quepy')
        self.assert_template_used('index.html')

    def test_nlquery_module(self):
        #result = self.app.get('/nlqueryengine')
        self.assert_template_used('index.html')

    def test_home_data(self):
        result = self.app.get('/')
        #assert the response data
        self.assert_template_used('index.html')

    def test_home_index_data(self):
        response = self.app.get('/', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    def test_static_question_external(self):
        response = self.app.get('/integratedstaticmessage', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    def static_question(self, sentence):
        return self.app.post('/integratedstaticmessage', data = sentence, follow_redirects = True)

    def dynamic_question(self, sentence):
        return self.app.post('/integrateddynamicmessage', data = sentence, follow_redirects = True)

    def test_dynamic_question_first(self):
        response = self.dynamic_question('What is the value of sensor1 in machine1?')
        self.assertEqual(response.status_code, 200)

    def test_static_question_first(self):
        response = self.static_question('What does linkedfactory contain?')
        self.assertEqual(response.status_code, 200)



    def test_quepy_answer(self):
        from MainFlask import quepySender
        sentence = "Who is Obama?"
        self.assertEqual(quepySender(str(sentence)), "hello")


if __name__ == "__main__":
    unittest.main()