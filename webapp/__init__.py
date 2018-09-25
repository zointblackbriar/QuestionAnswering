#Rest Service

from flask import Flask, request, render_template, jsonify, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from webapp.config import BaseConfig
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


RestService = Flask(__name__)
RestService.config.from_object(BaseConfig)

bcrypt = Bcrypt(RestService)
db = SQLAlchemy(RestService)

#Do not change this line
#Otherwise you will get a problem as below
#The problem is you are importing RestService before you are creating the instance of db in your __init__.py
#https://stackoverflow.com/questions/41828711/flask-blueprint-sqlalchemy-cannot-import-name-db-into-moles-file
from webapp.ModelWebApp import User

#routes

@RestService.route('/')
def flaskDevelopment():
    logger.warn(" render template is active")
    #return render_template('test.html')
    return RestService.send_static_file('index.html')

@RestService.route('/api/register', methods=['POST'])
def register():
    logger.info("register routing")
    json_data = request.json
    user = User(email = json_data['email'],
                password = json_data['password'])
    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'This user is already registered'
    db.session.close()
    return jsonify({'result' : status})

@RestService.route('/api/login', methods=['POST'])
def login():
    logger.info("login routing")
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash( user.password, json_data['password']):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'result': status})

@RestService.route('/api/logout')
def logout():
    logger.info("logout routing")
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})

@RestService.route('/api/status')
def status():
    logger.info("status routing")
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})


#To take info from text box
@RestService.route('/dbpedia', methods =['GET', 'POST'])
def my_form_post():
    print(request.is_json)
    content = request.get_json()
    print(content)
    #text = request.form['text']
    #processed_text = text.lower()
    #nltkWordFreq(processed_text)
    #clearTokenAndStopWords(processed_text)
    #You should return a response
    #return processed_text


@RestService.route('/', methods=['GET', 'POST' ])
def indexRestService():
    return render_template('test.html')


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
    RestService.run(debug = True)
