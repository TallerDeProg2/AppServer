from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse, abort
import requests
import logging
import src.main.global_method as gm
import jsonschema as js


app = Flask(__name__)


class Edit(Resource):
    def put(self, id, endpoint, schema):
        """Permite modificar"""
        gm.check_token(id)
        content = request.json
        try:
            js.validate(content, schema)
        except js.exceptions.ValidationError:
            logging.error('Argumentos ingresados inválidos')
            abort(400)

        try:
            r = requests.get(endpoint, headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error en get: ' + repr(r.status_code))
            abort(r.status_code)

        content['_ref'] = r.json()['user']['_ref']

        try:
            r = requests.put(endpoint, json=content, headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error en put: ' + repr(r.status_code))
            abort(r.status_code)

        return gm.build_response(r.json())

