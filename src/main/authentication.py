from flask import Flask
from flask_restful import Resource, reqparse, abort
import requests
from pymongo import MongoClient
import logging
from src.main.edit import validate_args
import src.main.global_method as gm

app = Flask(__name__)
parser = reqparse.RequestParser()

client = MongoClient('mongodb://sofafafa:sofafafa1@ds141098.mlab.com:41098/ubre')
db = client['ubre']
drivers_db = db['drivers_test']
passengers_db = db['passengers_test']


def send_post(endpoint, content):
    try:
        r = requests.post(endpoint, json=content)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
        abort(r.status_code)

    return r.json()


class HelloWorld(Resource):
    def get(self):
        return "Hola"


class LogIn(Resource):
    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'fb': {
                'type': 'object',
                'properties': {
                    'userID': {'type': 'string'},
                    'authToken': {'type': 'string'}
                },
                'required': ['userID', 'authToken']
            },
        },
        'required': ['username', 'password', 'fb']
    }

    def post(self):
        """Permite loggear un usuario"""
        content = validate_args(self.schema)

        r = send_post('direccionana/users/validate', content)

        #Crear token
        token = gm.encode_token(r['id'])
        r['token'] = token
        return r, 200
        # return content


class SignUpUser(Resource):
    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'fb': {
                'type': 'object',
                'properties': {
                    'userID': {'type': 'string'},
                    'authToken': {'type': 'string'}
                },
                'required': ['userID', 'authToken']
            },
            'firstName': {'type': 'string'},
            'lastName': {'type': 'string'},
            'country': {'type': 'string'},
            'email': {'type': 'string'},
            'birthdate': {'type': 'string'}
        },
        'required': ['username', 'password', 'fb', 'firstName', 'lastName',
                     'country', 'email', 'birthdate']
    }

    def post(self):
        """Permite registrar un usuario"""
        content = validate_args(self.schema)

        r = send_post('direccionana/users', content)

        if r['type'] == 'passenger':
            passengers_db.insert_one({'_id': r['id'], 'lat': '', 'long': ''})
        # passengers_db.insert_one({'_id': '238932', 'lat': '', 'long': ''})
        else:
            drivers_db.insert_one({'_id': r['id'], 'lat': '', 'long': ''})

        return r, 201
        # return content, 201

