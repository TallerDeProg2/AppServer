# -*- coding: utf-8 -*-
import datetime
import logging

import jsonschema as js
import requests
from flask import Flask, request, jsonify, make_response, Response
from flask_restful import Resource, abort

import src.main.constants.schemas as sch
import src.main.constants.shared_server as ss
from src.main import global_method as gm
from src.main.constants import mongo_spec as db
import requests
import src.main.constants.shared_server as ss

app = Flask(__name__)


class TripRequest(Resource):
    schema = sch.trips_full_schema

    def get(self, id):
        return "get Trip request"

    def post(self, id):
        """
        Crear una soliciud e viaje.
        :param id:
        :return json con id del viaje solicitado:
        """
        logging.info("[POST:/passengers/" + str(id) + "/trips/request] Trip Request.")
        token = request.headers['token']

        if gm.validate_token(token):
            logging.info("[POST:/passengers/" + str(id) + "/trips/request] El token es correcto")
            passenger = db.passengers.find_one({'_id': id})

            if passenger:
                logging.info("usuario correcto")
                content = request.get_json()

                try:
                    js.validate(content, self.schema)
                except js.exceptions.ValidationError:
                    logging.error('[POST:/passengers/' + str(id) + '/trips/request] Argumentos ingresados inválidos')
                    abort(400)

                # if self.is_passenger_alredy_has_some_trip_request():


                trip = self._convert_to_trip(id, content)
                self._add_trip_to_db(trip)

                logging.info('[POST:/passengers/' + str(id) + '/trips/request] Todo salio correcto')
                return make_response(jsonify(trip_id=trip['_id']), 201)

            else:
                logging.error('[POST:/passengers/' + str(id) + '/trips/request] Usuario no conectado')
                abort(404)
        else:
            logging.error('[POST:/passengers/' + str(id) + '/trips/request] Token invalido')
            abort(401)

    def _add_trip_to_db(self, trip):
        """
        Agrega el viaje en la base de datos,
        si la clave esta duplicada aborta con codigo de error 409
        :param trip:
        :return:
        """
        any_trip = db.trips.find_one({'passenger': trip['passenger'], 'status': 'available'})
        if any_trip:
            logging.error("[POST:/passengers/" + str(trip['passenger']) + "/trips/request] Ya posee una solicitud de viaje activa")
            abort(409) #TODO: ver que error tirar
        trip["_id"] = db.trips.count() + 1
        try:
            db.trips.insert_one(trip)
            # content["id"] = content.pop("_id")
        except db.errors.DuplicateKeyError:
            logging.error("[POST:/passengers/" + str(trip['passenger']) + "/trips/request] No se puedo completar la operacion")
            abort(409)


    def _convert_to_trip(self, id_passenger, content):
        """
        :param id_passenger:
        :param content:
        :return:
        """
        trip = {}
        trip["passenger"] = id_passenger
        trip["driver"] = ""
        trip["start"] = {}
        trip["start"]["street"] = content['trip']['legs'][0]['start_address']
        trip["start"]["location"] = {}
        trip["start"]["location"]["lat"] = content['trip']['legs'][0]['start_location']['lat']
        trip["start"]["location"]["lon"] = content['trip']['legs'][0]['start_location']['lng']
        trip["end"] = {}
        trip["end"]["street"] = content['trip']['legs'][0]['end_address']
        trip["end"]["location"] = {}
        trip["end"]["location"]["lat"] = content['trip']['legs'][0]['end_location']['lat']
        trip["end"]["location"]["lon"] = content['trip']['legs'][0]['end_location']['lng']
        trip["totalTime"] = 0
        trip["waitTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trip["travelTime"] = 0
        trip["distance"] = content['trip']['legs'][0]['distance']['value']
        trip["startTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trip["status"] = "available"
        trip["cost"] = {}
        trip["cost"]["currency"] = ""
        trip["cost"]["value"] = 0
        trip["directions"] = content['trip']
        return trip


#Chofer acepta viaje
class TripConfirmation(Resource):
    def post(self, id):
        """
            Deletes available trip from database and
            sets driver to not available

        """
        token = request.headers['token']
        if not gm.validate_token(token):
            logging.error('Token inválido')
            abort(401)

        content = request.json
        # try:
        #     js.validate(content, schema) #TODO Determinar schema
        # except js.exceptions.ValidationError:
        #     logging.error('Argumentos ingresados inválidos')
        #     abort(400)

        db.trips.update_one({'_id': content['trip_id']}, {
            '$set': {
                'driver': id,
                'status': 'inProgress'
            }
        })
        db.drivers.update_one({'_id': id}, {
            '$set': {
                'available': False
            }
        })
        pass_id = db.trips.find_one({'_id': content['trip_id']})['passenger']
        self.push_notification(id, pass_id)

        return Response(status=201)

    def push_notification(self, driver_id, pass_id):
        try:
            r = requests.get(ss.URL + '/users/' + str(driver_id), headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error en get: ' + repr(r.status_code))
            abort(r.status_code)
        driver_username = r.json()['user']['username']
        gm.push_notif(pass_id, "Viaje confirmado", "Su viaje está en camino, el conductor es " + driver_username)


class TripStart(Resource):
    def post(self, id):
        """
            Updates waiting time and start time

         """
        token = request.headers['token']
        if not gm.validate_token(token):
            logging.error('Token inválido')
            abort(401)

        trip = db.trips.find_one({'_id': id})
        start_time = datetime.datetime.now()
        start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")

        wait_time = datetime.datetime.now() - datetime.datetime.strptime(trip['waitTime'], "%Y-%m-%d %H:%M:%S")
        wait_time = round(wait_time.total_seconds())

        db.trips.update_one({'_id': id}, {
            '$set': {
                'waitTime': wait_time,
                'startTime': start_time
            }
        })
        return Response(status=201)


class TripEnd(Resource):
    def post(self, id):
        """
            Updates waiting time and start time

         """
        token = request.headers['token']
        if not gm.validate_token(token):
            logging.error('Token inválido')
            abort(401)

        content = request.json
        paymethod = content['paymethod']
        trip = db.trips.find_one({'_id': id})

        if paymethod == 'cash':
            properties = {'method': 'cash'}
        elif paymethod == 'card':
            properties = self.get_card(trip['passenger'])
        else:
            logging.error('Parámetro paymethod incorrecto: ' + paymethod)
            abort(400)

        start_datetime = datetime.datetime.strptime(trip['startTime'], "%Y-%m-%d %H:%M:%S")
        trip_time = datetime.datetime.now() - start_datetime
        trip_time = round(trip_time.total_seconds())

        cost = self.get_cost(trip['distance'], trip_time, paymethod, start_datetime, trip['startTime'])
        self.post_trip(trip, cost, trip_time, paymethod, properties)
        self.update_db(trip)
        gm.push_notif(trip['driver'], "Viaje terminado", "Esperamos que haya disfrutado su viaje")

        return {'cost': cost}, 201


    def get_card(self, id_passenger):
        try:
            r = requests.get(ss.URL + '/users/' + str(id_passenger) + '/card', headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error en post: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()['card']

    def get_cost(self, distance, trip_time, paymethod, start_datetime, start_time):
        payload = {
            'distance': distance,
            'traveltime': trip_time,
            'paymethod': paymethod,
            'day': start_datetime.strftime("%A"),
            'travelhour': start_time
        }
        try:
            r = requests.post(ss.URL + '/trips/estimate', json=payload, headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error en post: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()['cost']

    def post_trip(self, trip, cost, trip_time, paymethod, properties):
        ok = False
        trip['cost'] = cost
        trip['travelTime'] = trip_time
        trip['totalTime'] = trip_time + trip['waitTime']
        paymethod_json = {'paymethod': paymethod,
                          'parameters': properties}
        trip['paymethod'] = paymethod_json

        while not ok:
            ok = self.post_transaction(trip)

    def post_transaction(self, trip):
        payment_json = {'trip': trip['_id'],
                        'payment': {'value': trip['cost']['value'],
                                    'transaction_id': 'fhwufhwohji7',
                                    'currency': trip['cost']['currency'],
                                    'paymethod': trip['paymethod']['parameters']
                                    }
                        }
        try:
            r = requests.post(ss.URL + '/users/' + str(trip['passenger']) + '/transactions', json=payment_json,
                              headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            if r.status_code == 503:
                return False
            else:
                logging.error('Conexión con el Shared dio error en /users/' +
                              repr(trip['passenger']) + '/transactions: ' + repr(r.status_code))
                abort(r.status_code)
        return True

    def update_db(self, trip):
        db.drivers.update_one({'_id': trip['driver']}, {
            '$set': {
                'available': True
            }
        })
        db.trips.update_one({'_id': trip['_id']}, {
            '$set': {
                'status': 'finished',
                'travelTime': trip['travelTime'],
                'totalTime': trip['totalTime'],
                'cost': trip['cost']
            }
        })


class TripEstimate(Resource):
    schema = sch.trips_full_schema

    def get(self, id):
        return "get Trip estimate"

    def post(self):
        """Estimar un valor de viaje propuesto"""
        logging.info("post TripEstimate")
        token = request.headers['token']


        if gm.validate_token(token):
            logging.info("token correcto")

            content = request.get_json()
            if self._is_valid_body_request(content):
                query = self._filter_body(content)
                response = self._send_query(query)

                # todo: ver si solo le mando el costo o algo mas
                return make_response(jsonify(cost=response['cost'], token=token), 201)

            logging.error('Argumentos ingresados inválidos')
            abort(400)

        logging.error('Token invalido')
        abort(401)

    def _filter_body(self, content):
        now = datetime.datetime.now()
        travelhour = now.strftime("%Y-%m-%d %H:%M:%S ") + "ART"
        day = now.strftime("%A")
        distance = content['trip']['legs'][0]['distance']['value']
        duration = content['trip']['legs'][0]['duration']['value']
        pymethod = content['paymethod']
        return {'distance': distance, 'traveltime': duration,
                'paymethod': pymethod, 'day': day, 'travelhour': travelhour}

    def _send_query(self, query):
        try:
            r = requests.post(ss.URL + '/trips/estimate/', json=query, headers={'token': 'superservercito-token'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()

    def _is_valid_body_request(self, body):
        try:
            js.validate(body, self.schema)
        except js.exceptions.ValidationError:
            return False
        return True

