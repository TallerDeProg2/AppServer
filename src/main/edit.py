from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse, abort
import requests
import jsonschema as js
import logging
import src.main.global_method as gm
import src.main.constants.shared_server as ss
import src.main.constants.schemas as sch

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
    schema = sch.user_full_schema
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
    url = ss.URL + '/users/'


class EditCar(Edit):
    schema = sch.car_schema
    url = ss.URL + '/driver/'
    endpoint = '/cars'


class EditPayment(Edit):
    schema = sch.payment_schema
    url = ss.URL + '/passenger/'
    endpoint = '/payment'
