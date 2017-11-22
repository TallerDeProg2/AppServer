from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse, abort
import requests
import logging
import src.main.global_method as gm


app = Flask(__name__)


class Edit(Resource):
    def put(self, id, endpoint, schema):
        """Permite modificar"""
        gm.check_token(id)
        content = gm.validate_args(schema)
        r = requests.get(endpoint).json()
        content['_ref'] = r['_ref']

        try:
            r = requests.put(endpoint, json=content)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)

        return r.json()

