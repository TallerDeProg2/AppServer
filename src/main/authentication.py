from flask import Flask
from flask_restful import Resource, reqparse, abort
import requests
from pymongo import MongoClient
import logging
from src.main.edit import validate_args
from src.main.global_method import encode_token

app = Flask(__name__)
parser = reqparse.RequestParser()

client = MongoClient('localhost', 27017)
db = client.baseprueba
coll = db.baseprueba


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

        try:
            r = requests.post('direccionana/users/validate', json=content)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code) # Por ahi podria pasarle el error q me manda ana a alan
                                 #Ver si mandar error a alan o se manda solo
        #Crear token
        token = encode_token(r.json()['id'])
        return r.json()
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

        try:
            r = requests.post('direccionana/users', json=content)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)

        # Crear usuario en database, con formato de db
        # coll.insert_one('_id: 74748548, token: 8725889227')

        # return r.json()
        return content

