import logging

import requests
from flask import Flask
from flask_restful import Resource, abort
import src.main.constants.shared_server as ss

app = Flask(__name__)


class Get(Resource):
    def get(self,endpoint):
        try:
            r = requests.get(endpoint)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()


class GetDriver(Resource):
    def get(self, id):
        try:
            r = requests.get(ss.URL + '/users' + id)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()


class GetCar(Resource):
    def get(self, id):
        try:
            r = requests.get(ss.URL + '/users' + id + '/cars')
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()
