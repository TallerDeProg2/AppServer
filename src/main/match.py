# -*- coding: utf-8 -*-
# import src.main.constants.shared_server as ss
import logging

import jsonschema as js
from flask import Flask, request,jsonify, make_response
from flask_restful import Resource, abort

import src.main.constants.schemas as sch
from src.main import global_method as gm
from src.main.constants import mongo_spec as db
from datetime import datetime
import requests
import src.main.constants.shared_server as ss

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


#Chofer acepta viaje
class TripConfirmation(Resource):
    def post(self, id):
        """
            Deletes available trip from database and
            sets driver to not available

        """
        # token = request.headers['token']
        # if not gm.validate_token(token, id):
        #     logging.error('Token inválido')
        #     abort(401)

        content = request.json
        # try:
        #     js.validate(content, schema)
        # except js.exceptions.ValidationError:
        #     logging.error('Argumentos ingresados inválidos')
        #     abort(400)

        # db.trips.delete_one({'_id': content['trip']['id']})
        db.trips.update_one({'_id': content['trip']['id']}, {
            '$set': {
                'driver': id,
                'status': 'InProgress'
            }
        })
        db.drivers.update_one({'_id': id}, {
            '$set': {
                'available': False
            }
        })


        return 200


class TripStart(Resource):
    def post(self, id):
        """
            Updates waiting time and start time

         """
        trip = db.passengers.find_one({'_id': id})
        start_time = datetime.now()
        wait_time = datetime.now() - trip['waitTime']
        wait_time = round(wait_time.total_seconds())

        db.trips.update_one({'_id': id}, {
            '$set': {
                'waitTime': wait_time,
                'startTime': start_time
            }
        })


        return 200


class TripEnd(Resource):
    def post(self, id):
        """
            Updates waiting time and start time

         """
        content = request.json

        trip = db.trips.find_one({'_id': id})
        end_time = datetime.now()
        trip_time = datetime.now() - trip['startTime']
        trip_time = round(trip_time.total_seconds())
        total_distance = trip['google']['legs'][0]['distance']['value']

        if content['paymethod'] == 'cash':
            paymethod = 'cash'
        elif content['paymethod'] == 'card':
            paymethod = 'card'
            try:
                r = requests.get(ss.URL + '/user/' + trip['passenger'], headers={'token': 'superservercito-token'})
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                logging.error('Conexión con el Shared dio error en post: ' + repr(r.status_code))
                abort(r.status_code)
            properties = r['user']['card']
        else:
            logging.error('Parámetro paymethod incorrecto: ' + content['paymethod'])
            abort(400)


        payload = {
            'distance': total_distance,
            'traveltime': trip_time,
            'paymethod': content['paymethod'],
            'day': '',
            'travelhour': ''
        }

        try:
            r = requests.post(ss.URL + '/trips/estimate', json=payload, headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error en post: ' + repr(r.status_code))
            abort(r.status_code)

        total_cost = r['cost']

        try:
            r = requests.post(ss.URL + '/trips', json=payload, headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error en post: ' + repr(r.status_code))
            abort(r.status_code)

        db.drivers.update_one({'_id': content['driver']}, {
            '$set': {
                'available': True
            }
        })


        return 200
