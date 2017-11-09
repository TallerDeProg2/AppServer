from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse, abort
import requests
import jsonschema as js
import logging

app = Flask(__name__)


def validate_args(schema):
    content = request.json
    try:
        js.validate(content, schema)
    except js.exceptions.ValidationError:
        logging.error('Argumentos ingresados inválidos')
        abort(400)

    return content


def send_edit(endpoint, content):
    r = requests.get(endpoint).json()
    content['_ref'] = r['_ref']

    try:
        r = requests.put(endpoint, json=content)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
        abort(r.status_code)  # Por ahi podria pasarle el error q me manda ana a alan

    return r.json()



class EditUser(Resource):
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

    def put(self, id):
        """Permite modificar un usuario"""
        #validate_token(token, id) #Devuelve T o F, loggear
        content = request.json
        try:
            js.validate(content, self.schema)
        except js.exceptions.ValidationError:
            logging.error('Argumentos ingresados inválidos')
            abort(400)

        r = requests.get('direccionana/users/' + id).json()
        content['_ref'] = r['_ref']

        try:
            r = requests.put('direccionana/users/' + id, json=content)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code) # Por ahi podria pasarle el error q me manda ana a alan

        return r.json()


class EditCar(Resource):
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

    def put(self, id):
        """Permite modificar un auto"""
        # validate_token(token, id) #Devuelve T o F, loggear
        content = validate_args(self.schema)
        send_edit('direccionana/driver/' + id + '/cars', content)


class EditPayment(Resource):
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

    def put(self, id):
        """Permite modificar los datos de pago"""
        # validate_token(token, id) #Devuelve T o F, loggear
        content = validate_args(self.schema)
        send_edit('direccionana/passenger/' + id + '/payment', content) # Chequear endpoint con ana
