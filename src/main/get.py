import logging

import requests
from flask import Flask
from flask_restful import Resource, abort

app = Flask(__name__)


class Get(Resource):
    def get(self, endpoint):
        try:
            r = requests.get(endpoint, headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()

