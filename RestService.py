from flask import Flask, request, render_template, Blueprint
from Utils import *

RestService = Flask(__name__)

#RestServiceBlueprints = Blueprint('RestService', __name__)

##Test program for algorithm with web interface
#This will be integrated with ASPNET Web API

#Tokenization

@RestService.route('/')
def flaskDevelopment():
    return render_template('test.html')

#To take info from text box
@RestService.route('/', methods =['GET', 'POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.lower()
    nltkWordFreq(processed_text)
    clearTokenAndStopWords(processed_text)
    #You should return a response
    return processed_text




@RestService.route('/helloworld')
def helloWorld():
    return 'Hello World'

@RestService.route('/test/')
def test_list():
    return 'List all of items'

@RestService.route('/test/<int:test_id>/')
def getWithID(test_id):
    return 'Detail of Item  #{}.'.format(test_id)

@RestService.route('/test/<int:test_id>/delete/', methods=  ['DELETE'])
def test_delete(test_id):
    raise NotImplementedError('DELETE')

if __name__ == '__main__':
    RestService.run('0.0.0.0', debug=True)
