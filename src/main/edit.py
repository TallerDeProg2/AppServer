from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse, abort
import requests
import jsonschema as js
import logging

app = Flask(__name__)


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
                }
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
            abort(r.status_code)

        return r.json()
