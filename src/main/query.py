# -*- coding: utf-8 -*-
import logging
from math import radians, cos, sin, asin, sqrt

import requests
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, abort

import src.main.constants.shared_server as ss
from src.main import global_method as gm
from src.main.constants import mongo_spec as db

app = Flask(__name__)


# todo PASAR TODO A INGLES
class AvailableDrivers(Resource):
    max_distance = 25  # DEBERIA SETEARLA EL PASSENGER

    def get(self, id):
        logging.info("get AvailableDrivers")
        token = request.headers['token']

        if gm.validate_token(token):
            logging.info("token correcto")
            passenger = db.passengers.find_one({'_id': id})

            if passenger and passenger['lat'] != "" and passenger['lon'] != "":
                respuesta = {}
                respuesta['drivers'] = self._get_drivers_cercanos(passenger)
                respuesta['token'] = token
                return make_response(jsonify(drivers=respuesta, token=token), 200)

            logging.error('Id inexistente/no conectado')
            abort(404)

        logging.error('Token invalido')
        abort(401)

    def _calculate_distance(self, passenger, driver):
        """
            Calculate the great circle distance between two points
            on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        logging.info("Calcula distancia entre pasajero y conductor")
        # convert decimal degrees to radians
        londriver, latdriver = driver['lon'], driver['lat']
        lonpassenger, latpassenger = passenger['lon'], passenger['lat']
        lon_p, lat_p, lon_d, lat_d = map(radians,
                                         [float(lonpassenger), float(latpassenger), float(londriver), float(latdriver)])

        lon_distance = lon_d - lon_p
        lat_distance = lat_d - lat_p
        a = sin(lat_distance / 2) ** 2 + cos(lat_p) * cos(lat_d) * sin(lon_distance / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def _get_drivers_cercanos(self, passenger):
        cercanos = []
        for x in db.drivers.find({'available': True}):
            if self._calculate_distance(passenger, x) < self.max_distance:
                r = self._get_data_user(x['id'])
                cercanos.append({'driver': r['user'], 'position': {'lat': x['lat'], 'lon': x['lon']}})

        return cercanos

    def _get_data_user(self, _id):
        try:
            r = requests.get(ss.URL + '/users/' + str(id), headers={'token': "superservercito-token"})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()


class AvailableTrips(Resource):
    max_distance = 2  # DEBERIA SETEARLA EL PASSENGER

    def get(self, id):
        logging.info("get Available Trips")
        token = request.headers['token']

        if gm.validate_token(token):
            logging.info("token correcto")
            driver = db.drivers.find_one({'_id': id})

            if driver and driver['lat'] != "" and driver['lon'] != "":
                respuesta = self._get_trips(driver)
                return make_response(jsonify(trips=respuesta, token=token), 200)

            logging.error('Id inexistente/no conectado')
            abort(404)

        else:
            logging.error('Token invalido')
            abort(401)

    def _calculate_distance(self, passenger, driver):
        """
            Calculate the great circle distance between two points
            on the earth (specified in decimal degrees)
        """
        logging.info("Calcula distancia entre pasajero y conductor")
        # convert decimal degrees to radians
        londriver, latdriver = driver['lon'], driver['lat']
        lonpassenger, latpassenger = passenger['lon'], passenger['lat']
        lon_p, lat_p, lon_d, lat_d = map(radians,
                                         [float(lonpassenger), float(latpassenger), float(londriver), float(latdriver)])

        lon_distance = lon_d - lon_p
        lat_distance = lat_d - lat_p
        a = sin(lat_distance / 2) ** 2 + cos(lat_p) * cos(lat_d) * sin(lon_distance / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def _esta_cerca(self, passenger, driver):
        logging.info("filtra si estan cerca")
        return self._calculate_distance(passenger, driver) < self.max_distance

    def _get_trips(self, driver):
        logging.info("obtener los viajes disponibles y choferes mas cercanos")
        cercanos = []
        for x in db.trips.find({'status': 'available'}):
            passenger = db.passengers.find_one({'_id': x['passenger']})
            if self._is_valid_passenger(passenger) and self._esta_cerca(passenger, driver):
                r = self._get_data_user(passenger['_id'])
                # x['directions'] porque solo le mando la direccion de google
                cercanos.append({'passenger': r['user'], 'trip': x['directions'], 'id': x['_id']})
        return cercanos

    def _get_data_user(self, id):
        logging.info("pedir informacion del pasajero a shared")
        try:
            r = requests.get(ss.URL + '/users/' + str(id), headers={'token': "superservercito-token"})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        # r["id"] = r.pop("_id")
        return r.json()

    def _is_valid_passenger(self, passenger):
        return passenger and passenger['lat'] != "" and passenger['lon'] != ""


class TripHistory(Resource):
    def get(self, id, user_type):
        logging.info("get Trip History")

        token = request.headers['token']
        if not gm.validate_token(token, id):
            logging.error('Token inválido')
            abort(401)
        # token = 2

        logging.info("token correcto")
        if user_type == 'passenger':
            user = db.passengers.find_one({'_id': id})
        else:
            user = db.drivers.find_one({'_id': id})

        # if user:
        respuesta = self._get_trips(id)
        return make_response(jsonify(trips=respuesta, token=token), 200)
        # else:
        # logging.error('Id inexistente/no conectado')
        # abort(404)

    def _get_trips(self, id, type):
        logging.info("Obtener el historial de viajes del usuario")
        trip_history = []
        for x in db.trips.find({type: id, 'status': 'finished'}):
            trip_history.append(x)
        return trip_history


class PassengerTripHistory(Resource):
    def get(self, id):
        service = TripHistory()
        return service.get(id, 'passenger')


class DriverTripHistory(Resource):
    def get(self, id):
        service = TripHistory()
        return service.get(id, 'driver')
