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


class AvailableDrivers(Resource):
    max_distance = 2

    def get(self, id):
        """
        Choferes mas cercanos para un passenger
        :param id:
        :return lista con la informacion de los choferes:
        """
        logging.info("[GET:/passengers/"+ id+ "/drivers] Available Drivers.")
        token = request.headers['token']

        if gm.validate_token(token):
            logging.info("[GET:/passengers/"+ id+ "/drivers] El token es correcto")

            # puede ingresar opcionalmente por parametro el radio de busqueda de los viajes en km
            # sino por default son 2 km
            # distance = request.args['max_distance']
            # if distance: self.max_distance = distance
            try:
                passenger = db.passengers.find_one({'_id': id})
            except db.errors.ConnectionFailure:
                logging.error('[GET:/passengers/'+ id+ '/drivers] Fallo de conexion con la base de datos')
                abort(500)

            if self._is_valid_user(passenger):
                response = {}
                response['drivers'] = self._get_closer_drivers(passenger)
                response['token'] = token
                logging.info('[GET:/passengers/'+ id+ '/drivers] Todo salio correcto')
                return make_response(jsonify(response), 200)

            logging.error('[GET:/passengers/'+ id+ '/drivers] Usuario no conectado')
            abort(404)

        logging.error('[GET:/passengers/'+ id+ '/drivers] Token invalido')
        abort(401)

    def _calculate_distance(self, passenger, driver):
        """
        Calcula la distancia entre un driver y un passenger
        :param passenger:
        :param driver:
        :return km de separcion entre el chofer y el pasajero:
        """
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

    def _get_closer_drivers(self, passenger):
        """
        Retorna una lista con los choferes disponibles mas cercanos en un radio de max_distance
        :param passenger:
        :return lista de json {'driver':, 'position': {'lat': , 'lon': }}:
        """
        logging.info("[_get_closer_drivers] Busca los choferes cercanos.")
        nearest = []
        for driver in db.drivers.find({'available': True}):
            if self._calculate_distance(passenger, driver) < self.max_distance:
                user_data = self._get_data_user(driver['_id'])
                nearest.append({'driver': user_data['user'], 'position': {'lat': driver['lat'], 'lon': driver['lon']}})
        logging.info("[_get_closer_drivers] Se encontraron "+str(len(nearest))+ " choferes cercanos.")
        return nearest

    def _get_data_user(self, id):
        """
        Obtiene del Shared server los datos del usuario,
        si hay un error se aborta con el mismo status-code
        :param id:
        :return json con los datos del usuario:
        """
        logging.info("[_get_data_user] Pide la informacion del usuario al Shared server")
        try:
            response = requests.get(ss.URL + '/users/' + str(id), headers={'token': "superservercito-token"})
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('[_get_data_user] Conexión con el Shared dio error: ' + repr(response.status_code))
            abort(response.status_code)
        logging.info("[_get_data_user] La consulta al Shared fue correcta.")
        return response.json()

    def _is_valid_user(self, user):
        """
        El usuario es valido cuando no es None y su latitud y longitud no estan vacias
        :param user:
        :return bool:
        """
        return user and user['lat'] != "" and user['lon'] != ""


class AvailableTrips(Resource):
    max_distance = 2  # DEBERIA SETEARLA EL PASSENGER

    def get(self, id):
        """
        Viajes disponibles mas cercanos para un driver
        :param id:
        :return lista de viajes con la informacion del pasajero:
        """
        logging.info("[GET:/drivers/"+id+"/trips] Available Trips.")
        token = request.headers['token']

        if gm.validate_token(token):
            logging.info("[GET:/drivers/"+id+"/trips] El token es correcto")

            # puede ingresar opcionalmente por parametro el radio de busqueda de los viajes en km
            # sino por default son 2 km
            # distance = request.args['max_distance']
            # if distance: self.max_distance = distance

            try:
                driver = db.drivers.find_one({'_id': id})
            except db.errors.ConnectionFailure:
                logging.error('[GET:/drivers/'+id+'/trips] Fallo de conexion con la base de datos')
                abort(500)

            if self._is_valid_user(driver):
                respuesta = self._get_trips(driver)
                logging.info('[GET:/drivers/'+id+ '/trips] Todo salio correcto')
                return make_response(jsonify(trips=respuesta, token=token), 200)

            logging.error('[GET:/drivers/'+id+'/trips] Usuario no conectado')
            abort(404)

        else:
            logging.error('[GET:/drivers/'+id+'/trips] Token invalido')
            abort(401)

    def _calculate_distance(self, passenger, driver):
        """
        Calcula la distancia entre un driver y un passenger
        :param passenger:
        :param driver:
        :return km de separcion entre el chofer y el pasajero:
        """
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

    def _is_closer(self, passenger, driver):
        return self._calculate_distance(passenger, driver) < self.max_distance

    def _get_trips(self, driver):
        logging.info("[_get_trips] Busca los viajes cercanos.")
        nearest = []
        for x in db.trips.find({'status': 'available'}):
            passenger = db.passengers.find_one({'_id': x['passenger']})
            if self._is_valid_user(passenger) and self._is_closer(passenger, driver):
                r = self._get_data_user(passenger['_id'])
                # x['directions'] porque solo le mando la direccion de google'passenger': r['user']
                nearest.append({'id': x['_id'], 'trip': x['directions'], 'passenger': r['user']})
        logging.info("[_get_trips] Se encontraron "+str(len(nearest))+ " viajes cercanos.")
        return nearest

    def _get_data_user(self, id):
        """
        Obtiene del Shared server los datos del usuario,
        si hay un error se aborta con el mismo status-code
        :param id:
        :return json con los datos del usuario:
        """
        logging.info("[_get_data_user] Pide la informacion del usuario al Shared server")
        try:
            response = requests.get(ss.URL + '/users/' + str(id), headers={'token': "superservercito-token"})
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('[_get_data_user] Conexión con el Shared dio error: ' + repr(response.status_code))
            abort(response.status_code)
        logging.info("[_get_data_user] La consulta al Shared fue correcta.")
        return response.json()

    def _is_valid_user(self, user):
        """
        El usuario es valido cuando no es None y su latitud y longitud no estan vacias
        :param user:
        :return bool:
        """
        return user and user['lat'] != "" and user['lon'] != ""


class TripHistory(Resource):
    def get(self, id, user_type):
        logging.info("get Trip History")

        token = request.headers['token']
        if not gm.validate_token(token, id):
            logging.error('Token inválido')
            abort(401)

        logging.info("Token correcto")
        if user_type == 'passenger':
            user = db.passengers.find_one({'_id': id})
        else:
            user = db.drivers.find_one({'_id': id})

        if user:
            respuesta = self._get_trips(id, user_type)
        else:
            logging.error('Id inexistente/no conectado')
            abort(404)
        return make_response(jsonify(trips=respuesta, token=token), 200)

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
