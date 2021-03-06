from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse, abort
import requests
import logging
import src.main.global_method as gm
import jsonschema as js


app = Flask(__name__)


class Edit(Resource):
    def put(self, id, endpoint, schema, type=None):
        """Permite modificar"""
        token = request.headers['token']
        if not gm.validate_token(token, id):
            logging.error('Token invalido')
            abort(401)

        content = request.json
        if not gm.validate_args(schema, content):
            abort(400)

        if type == 'user' or type == 'car':
            content = self.add_ref(endpoint, content, type)

        try:
            r = requests.put(endpoint, json=content, headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error en put: ' + repr(r.status_code))
            print(r.json())
            abort(r.status_code)
        return r.json()

    def add_ref(self, endpoint, content, type):
        try:
            r = requests.get(endpoint, headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error en get: ' + repr(r.status_code))
            abort(r.status_code)

        content['_ref'] = r.json()[type]['_ref']
        return content

