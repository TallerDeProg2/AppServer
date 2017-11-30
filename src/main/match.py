# -*- coding: utf-8 -*-
# import src.main.constants.shared_server as ss
import datetime
import logging

import jsonschema as js
import requests
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, abort

import src.main.constants.schemas as sch
import src.main.constants.shared_server as ss
from src.main import global_method as gm
from src.main.constants import mongo_spec as db


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
            # todo: hacerlo mejor...
            content["id"] = content.pop("_id")
            return True
        except db.errors.DuplicateKeyError:
            return False


class TripEstimate(Resource):
    def get(self, id):
        return "get Trip estimate"

    def post(self):
        """Estimar un valor de viaje propuesto"""
        logging.info("post TripEstimate")
        token = request.headers['token']

        # todo FALTAN LAS VALIDACIONES DE LO QUE RECIBO DE ALAN
        if gm.validate_token(token):
            logging.info("token correcto")

            content = request.get_json()
            query = self._filter_body(content)
            response = self._send_query(query)

            # todo: ver si solo le mando el costo o algo mas
            return make_response(jsonify(cost=response['cost'], token=token), 201)
        else:
            logging.error('Token invalido')
            abort(401)

    def _filter_body(self, content):
        now = datetime.datetime.now()
        travelhour = now.strftime("%Y-%m-%d %H:%M:%S ") + "ART"
        day = now.strftime("%d") #TODO hacer que no mande el dia en numero
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
