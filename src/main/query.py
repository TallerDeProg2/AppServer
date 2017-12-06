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


# TODO MANDAR POSITION = {LAT, LON} VER DE AGRUPAR EN GENERAL EN BASE
class AvailableDrivers(Resource):
    def get(self, id):
        logging.info("get AvailableDrivers")
        token = request.headers['token']

        if gm.validate_token(token):
            logging.info("token correcto")
            passenger = db.passengers.find_one({'id': id})

            if passenger:
                if passenger['lat'] != "" and passenger['lon'] != "":
                    respuesta = self._get_drivers_cercanos(passenger)
                    respuesta['token'] = token
                    return make_response(jsonify(respuesta), 200)
                else:
                    logging.error('no tiene ubicacion')
                    abort(400)

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
        # convert decimal degrees to radians
        londriver, latdriver = driver['lon'], driver['lat']
        lon_p, lat_p, lon_d, lat_d = map(radians, [int(passenger['lon'])
            , int(passenger['lat']), int(londriver), int(latdriver)])
        lon_distance = lon_d - lon_p
        lat_distance = lat_d - lat_p
        a = sin(lat_distance / 2) ** 2 + cos(lat_p) * cos(lat_d) * sin(lon_distance / 2) \
                                                                   ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        # return km
        return int(londriver) + int(latdriver)

    def _esta_cerca(self, passenger, driver):
        max_distance = 25  # DEBERIA SETEARLA EL PASSENGER
        if self._calculate_distance(passenger, driver) < max_distance:
            return True
        return False

    def _get_drivers_cercanos(self, passenger):
        cercanos = []
        for x in db.drivers.find({}, {'_id': 0, 'token': 0}):
            if self._esta_cerca(passenger, x):
                # todo ver el tema del id _id si tenemos los dos y no mostramos el dafault de mongo o que ondis
                # r = self._get_data_user(x['id'])
                # cercanos.append(jsonify(driver=r, position={'lat': x['lat'], 'lon': x['lon']}))
                cercanos.append(x)
        return cercanos

    def _get_data_user(self, id):
        try:
            # todo hacer global el dominio de ana y apendearlo antes del endpoint
            r = requests.get('users/' + id, headers={'token': "alguntokenguardado"})
            # todo le tengo que mandar el token por header
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r


class AvailableTrips(Resource):
    max_distance = 2  # DEBERIA SETEARLA EL PASSENGER
    def get(self, id):
        logging.info("get Available Trips")
        token = request.headers['token']

        if gm.validate_token(token):
            logging.info("token correcto")
            driver = db.drivers.find_one({'_id': id})

            if driver:
                if driver['lat'] != "" and driver['lon'] != "":
                    respuesta = self._get_trips(driver)
                    # repuesta = self._get_drivers_cercanos(driver)
                    # respuesta['token'] = token
                    return make_response(jsonify(trips=respuesta, token=token), 200)
                else:
                    logging.error('sin ubicacion')
                    # TODO ver que error corresponde aca y el de arriba
                    abort(400)

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
        a = sin(lat_distance / 2) ** 2 + cos(lat_p) * cos(lat_d) * sin(lon_distance / 2) \
                                                                   ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def _esta_cerca(self, passenger, driver):
        logging.info("filtra si estan cerca")
        if self._calculate_distance(passenger, driver) < self.max_distance:
            return True
        return False

    def _get_trips(self, driver):
        logging.info("obtener los viajes disponibles y choferes mas cercanos")
        cercanos = []
        for x in db.trips.find({'status': 'available'}):
            passenger = db.passengers.find_one({'_id': x['passenger']})
            if self._is_valid_passenger(passenger) and self._esta_cerca(passenger, driver):
                r = self._get_data_user(passenger['_id'])
                # x['directions'] porque solo le mando la direccion de google
                cercanos.append(jsonify(passenger=r, trip=x['directions']))
        return cercanos

    def _get_data_user(self, id):
        logging.info("pedir informacion del pasajero a shared")
        try:
            r = requests.get(ss.URL + '/users/' + str(id), headers={'token': "superservecito-token"})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        # r["id"] = r.pop("_id")
        return r

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


        #if user:
        respuesta = self._get_trips(id)
        return make_response(jsonify(trips=respuesta, token=token), 200)
        #else:
        #logging.error('Id inexistente/no conectado')
        #abort(404)

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
