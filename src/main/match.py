# -*- coding: utf-8 -*-
# import src.main.constants.shared_server as ss
import logging

import jsonschema as js
from flask import Flask, request,jsonify, make_response
from flask_restful import Resource, abort

import src.main.constants.schemas as sch
from src.main import global_method as gm
from src.main.constants import mongo_spec as db

# {
#         "username": "aye", "trip": {   "start": {"lat": 0,  "lon": 0 }, "end":  { "lat": 1, "lon": 1 }    },  "paymethod": {  "paymethod": "efectivo" }
# }


app = Flask(__name__)


class TripRequest(Resource):
    schema = sch.trip_request_schema

    def get(self, id):
        return "todo ok"

    def post(self, id):
        """Registar una solicitud de viaje"""
        logging.info("post TripRequest")
        token = request.headers['token']

        if gm.validate_token(token):
            logging.info("token correcto")
            passenger = db.passengers.find_one({'_id': id})

            if passenger:
                logging.info("usuario correcto")
                content = request.get_json()
                if self._is_valid_body_request(content):
                    if self._add_trip_to_db(id, content):
                        # todo HACER RESPUESTA GENERICA Y RESPONDER CON ESO
                        content['token'] = token
                        return make_response(jsonify(content), 201)
                    else:
                        logging.error('Error ya tiene registrada una solicitud de viaje')
                        abort(409)
                else:
                    logging.error('Argumentos ingresados inválidos')
                    abort(400)
            else:
                logging.error('Id inexistente/no conectado')
                abort(404)
        else:
            logging.error('Token invalido')
            abort(401)

            #
            # content = validate_args(self.schema)
            #
            # content['_ref'] = '327378'
            #
            # r = send_post(ss.URL + '/users', content)
            #
            # if content['type'] == 'passenger':
            #     db.passengers.insert_one({'_id': r['user']['id'], 'lat': '', 'lon': ''})
            # elif content['type'] == 'driver':
            #     db.drivers.insert_one({'_id': r['user']['id'], 'lat': '', 'lon': ''})
            # else:
            #     logging.error('Parámetro type incorrecto: ' + content['type'])
            #     abort(400)
            #
            # return r, 201
            # # return content, 201

    def _is_valid_body_request(self, body):

        try:
            js.validate(body, self.schema)
        except js.exceptions.ValidationError:
            return False
        return True

    def _add_trip_to_db(self, id_passenger, content):
        # content["_id"] = db.trips.count()+1
        content["_id"] = id_passenger
        try:
            db.trips.insert_one(content)
            #todo: hacerlo mejor...
            content["id"] = content.pop("_id")
            return True
        except db.errors.DuplicateKeyError:
            return False


        # def validate_args(schema):
        #     content = request.json
        #     try:
        #         js.validate(content, schema)
        #     except js.exceptions.ValidationError:
        #         logging.error('Argumentos ingresados inválidos')
        #         abort(400)
        #
        #     return content
