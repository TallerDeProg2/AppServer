from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse, abort
import requests
import jsonschema as js
import logging
import src.main.global_method as gm
import src.main.constants.shared_server as ss

app = Flask(__name__)


def validate_args(schema):
    content = request.json
    try:
        js.validate(content, schema)
    except js.exceptions.ValidationError:
        logging.error('Argumentos ingresados inválidos')
        abort(400)

    return content


def validate_token(id):
    token = request.headers['token'] #Ver si esto bien o mal
    if not gm.validate_token(token, id):
        logging.error('Token inválido')
        abort(401)


class Edit(Resource):
    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'fb': {
                'type': 'object',
                'properties': {
                    'userId': {'type': 'string'},
                    'authToken': {'type': 'string'}
                },
                'required': ['userId', 'authToken']
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
    url = ss.URL
    endpoint = ''

    def put(self, id):
        """Permite modificar"""
        validate_token(id)
        content = validate_args(self.schema)
        r = requests.get(self.url + id + self.endpoint).json()
        content['_ref'] = r['_ref']

        try:
            r = requests.put(self.url + id + self.endpoint, json=content)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)

        return r.json()


class EditUser(Edit):
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
    url = ss.URL + '/users/'


class EditCar(Edit):
    schema = {
        'type': 'object',
        'properties': {
            'brand': {'type': 'string'},
            'model': {'type': 'string'},
            'color': {'type': 'string'},
            'plate': {'type': 'string'},
            'year': {'type': 'string'},
            'status': {'type': 'string'},
            'radio': {'type': 'string'},
            'airconditioner': {'type': 'boolean'}
        },
        'required': ['brand', 'model', 'color', 'plate', 'year',
                     'status', 'radio', 'airconditioner']
    }
    url = ss.URL + '/driver/'
    endpoint = '/cars'


class EditPayment(Edit):
    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'number': {'type': 'string'},
            'type': {'type': 'string'},
            'expirationMonth': {'type': 'string'},
            'expirationYear': {'type': 'string'}
        },
        'required': ['name', 'number', 'type', 'expirationMonth', 'expirationYear']
    }
    url = ss.URL + '/passenger/'
    endpoint = '/payment'
