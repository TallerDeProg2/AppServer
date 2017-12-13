import logging
import requests
from flask import Flask, request, Response
from flask_restful import Resource, abort
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
        logging.info("se loggea el chau")
        logging.error("Ahora un error")
        logging.warning("Ahora un warning")
        logging.debug("Ahora sale el debug")
        return "Chau"


class LogIn(Resource):
    schema = sch.user_reduced_schema

    def post(self):
        """Permite loggear un usuario"""
        content = request.json
        if not gm.validate_args(self.schema, content):
            abort(400)

        r = send_post(ss.URL + '/users/validate', content)

        token = gm.encode_token(r['user']['id'])
        response = gm.build_response(r)
        response['token'] = token
        return response, 201


class SignUpUser(Resource):
    schema = sch.user_full_schema

    def post(self):
        """Permite registrar un usuario"""
        content = request.json
        if not gm.validate_args(self.schema, content):
            abort(400)

        content['_ref'] = ''

        r = send_post(ss.URL + '/users', content)

        if content['type'] == 'passenger':
            db.passengers.insert_one({'_id': r['user']['id'], 'lat': '', 'lon': ''})
        elif content['type'] == 'driver':
            db.drivers.insert_one({'_id': r['user']['id'], 'lat': '', 'lon': '', 'available': True})
        else:
            logging.error('Parámetro type incorrecto: ' + content['type'])
            abort(400)

        logging.info('Usuario id: ' + repr(r['user']['id']) + ' creado en base ' + content['type'])
        #TODO: No esta loggeando

        return gm.build_response(r), 201


class LogOut(Resource):
    schema = sch.user_reduced_schema

    def post(self,id):
        """
        Permite que el usuario cierre sesion
        :param id:
        :return:
        """
        logging.info("[POST:/users/" + str(id) + "/logout] LogOut.")
        token = request.headers['token']

        if gm.validate_token(token, id):
            logging.info("[POST:/passengers/" + str(id) + "/drivers] El token es correcto")

            try:
                db.drivers.update_one({'_id': id}, {
                    '$set': {
                        'available': False
                    }
                })
            except db.errors.ConnectionFailure:
                logging.error('[POST:/users/' + str(id) + '/logout] Fallo de conexion con la base de datos')
                abort(500)

            return Response(status=201)

        logging.error('[POST:/users/' + str(id) + '/logout] Token invalido')
        abort(401)
