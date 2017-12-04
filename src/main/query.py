# -*- coding: utf-8 -*-
import logging
from math import radians, cos, sin, asin, sqrt

import requests
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, abort

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
            passenger = db.passengers.find_one({'_id': id})

            if passenger:
                repuesta = self._get_drivers_cercanos(passenger)
                return make_response(jsonify(RESPONSE=repuesta, token=token), 200)

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
        lon_p, lat_p, lon_d, lat_d = map(radians, [float(passenger['lon'])
            , float(passenger['lat']), float(londriver), float(latdriver)])
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
                # r = self._get_data_user(x['_id'])
                # cercanos.append(jsonify(driver=r, position={'lat': x['lat'], 'lon': x['lon']}))
                cercanos.append(x)
        return cercanos

    def _get_data_user(self, _id):
        try:
            # todo hacer global el dominio de ana y apendearlo antes del endpoint
            r = requests.get('users/' + _id, headers={'token': 'app.token'})
            # todo le tengo que mandar el token por header
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r


class AvailableTrips(Resource):
    def get(self, id):
        logging.info("get AvailableTrips")
        token = request.headers['token']

        if gm.validate_token(token):
            logging.info("token correcto")
            driver = db.drivers.find_one({'_id': id})

            if driver:
                repuesta = self._get_trips(driver)
                # repuesta = self._get_drivers_cercanos(driver)
                return make_response(jsonify(RESPONSE=repuesta, token=token), 200)

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
        lon_p, lat_p, lon_d, lat_d = map(radians, [float(passenger['lon'])
            , float(passenger['lat']), float(londriver), float(latdriver)])
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

    def _get_trips(self, driver):
        cercanos = []
        for x in db.trips.find():
            passenger = db.passengers.find_one({'_id': x['passenger']}) #todo ver nombre
            # todo error si no esta el passagero en base
            if passenger and self._esta_cerca(passenger, driver):
                # todo ver el tema del id _id si tenemos los dos y no mostramos el dafault de mongo o que ondis
                # r = self._get_data_user(x['_id'])
                # cercanos.append(jsonify(driver=r, position={'lat': x['lat'], 'lon': x['lon']}))
                cercanos.append(x)
        return cercanos

    def _get_data_user(self, id):
        try:
            # todo hacer global el dominio de ana y apendearlo antes del endpoint
            r = requests.get('users/' + id, headers={'token': 'app.token'})
            # todo le tengo que mandar el token por header
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r



# todo  el tema de los viajes disponibles es igual que el de choferes??
