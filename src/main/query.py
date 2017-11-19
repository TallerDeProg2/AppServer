from math import radians, cos, sin, asin, sqrt
from flask import Flask, request, jsonify
from flask_restful import Resource
from bson.objectid import ObjectId
from src.main import global_method as gm
from src.main import mongo_spec as db

app = Flask(__name__)


class AvailableDrivers(Resource):
    def get(self, _id):
        # LOG INFO - get choferes disponibles
        token = request.headers['token']

        if gm.validate_token(token):
            # LOG INFO - correct token
            passenger = db.passengers.find_one({'_id': ObjectId(_id)})

            # TODO: Handle passenger not found
            # if passenger == None:
            #   response 404, notifyError(), throwException(), something()...

            self._update_location(passenger)
            repuesta = self._get_drivers_cercanos(passenger)

            # r = requests.put('direccionana/users/' + id, json=r)
            # r.raise_for_status()

            return jsonify({"RESPONSE": repuesta, "token": token})
        else:
            # LOG ERROR - incorrect token
            return jsonify({"RESPONSE": "error"})

    def _get_actual_location(self, passenger):
        lat_passenger = request.args.get('lat')
        lon_passenger = request.args.get('lon')

        if (not lat_passenger or not lon_passenger) and (not passenger['lat'] or not passenger['lon']):
            # LOG ERROR - no existe ubicacion
            return jsonify({"RESPONSE": "no tiene posicion de inicio"})
        if not lat_passenger or not lon_passenger:
            # LOG WARNING - ultimo origen registrado
            return passenger['lat'], passenger['lon']
        return request.args.get('lat'), request.args.get('lon')

    def _update_location(self, passenger):  # DEBERIA SER [GLOBAL]
        """
            Set de concurrent location of user in database
        :param passenger:
        :return:
        """
        lat, lon = self._get_actual_location(passenger)
        db.passengers.find_one_and_update({"_id": passenger['_id']},
                                       {'$set': {"lat": lat, 'lon': lon}})

    def _calculate_distance(self, passenger, londriver, latdriver):
        """
            Calculate the great circle distance between two points
            on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
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

    def _esta_cerca(self, passenger, londriver, latdriver):
        max_distance = 25  # DEBERIA SETEARLA EL PASSENGER
        if self._calculate_distance(passenger, londriver, latdriver) < max_distance:
            return True
        return False

    def _get_drivers_cercanos(self, passenger):
        cercanos = []
        for x in db.drivers.find():
            if self._esta_cerca(passenger, x['lon'], x['lat']):
                cercanos.append({'lon': x['lon'], 'lat': x['lat']})
        return cercanos
