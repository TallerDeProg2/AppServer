import logging
import requests
from flask import Flask
from flask_restful import Resource, reqparse, abort
import src.main.constants.mongo_spec as db
import src.main.global_method as gm
from src.main.edit import validate_args
import src.main.constants.shared_server as ss
import src.main.constants.schemas as sch

app = Flask(__name__)
parser = reqparse.RequestParser()


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
        content = validate_args(self.schema)

        r = send_post(ss.URL + '/users/validate', content)

        #Crear token
        token = gm.encode_token(r['id'])
        r['token'] = token
        return r, 200
        # return content


class SignUpUser(Resource):
    schema = sch.user_full_schema

    def post(self):
        """Permite registrar un usuario"""
        content = validate_args(self.schema)

        content['_ref'] = '327378' #TODO: Ver que mandarle

        r = send_post(ss.URL + '/users', content)

        if content['type'] == 'passenger':
            db.passengers.insert_one({'_id': r['user']['id'], 'lat': '', 'lon': ''})
        # db.passengers.insert_one({'_id': '238932', 'lat': '', 'lon': ''})
        else:
            db.drivers.insert_one({'_id': r['user']['id'], 'lat': '', 'lon': ''})

        return r, 201
        # return content, 201

