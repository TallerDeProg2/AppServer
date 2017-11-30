import logging
import requests
from flask import Flask
from flask_restful import Resource, reqparse, abort
import src.main.constants.mongo_spec as db
import src.main.global_method as gm
import src.main.constants.shared_server as ss
import src.main.constants.schemas as sch

app = Flask(__name__)


def send_post(endpoint, content):
    try:
        r = requests.post(endpoint, json=content, headers={'token': 'superservercito-token'})
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
        logging.error('     Mensaje: ' + r.content.decode('utf-8', 'ignore'))
        abort(r.status_code)

    return r.json()


class HelloWorld(Resource):
    def get(self):
        return "Hola"


class ByeWorld(Resource):
    def get(self):
        return "Chau"


class LogIn(Resource):
    schema = sch.user_reduced_schema

    def post(self):
        """Permite loggear un usuario"""
        content = gm.validate_args(self.schema)

        r = send_post(ss.URL + '/users/validate', content)

        token = gm.encode_token(r['user']['id'])
        response = gm.build_response(r)
        response['token'] = token
        return response, 200


class SignUpUser(Resource):
    schema = sch.user_full_schema

    def post(self):
        """Permite registrar un usuario"""
        content = gm.validate_args(self.schema)

        content['_ref'] = ''

        r = send_post(ss.URL + '/users', content)
        print(r)

        if content['type'] == 'passenger':
            db.passengers.insert_one({'_id': r['user']['id'], 'lat': '', 'lon': ''})
        elif content['type'] == 'driver':
            db.drivers.insert_one({'_id': r['user']['id'], 'lat': '', 'lon': ''})
        else:
            logging.error('Parámetro type incorrecto: ' + content['type'])
            abort(400)

        logging.info('Usuario id: ' + repr(r['user']['id']) + ' creado en base ' + content['type'])
        #TODO: No esta loggeando
        response = gm.build_response(r)
        return r, 201

