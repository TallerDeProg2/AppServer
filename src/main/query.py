from math import radians, cos, sin, asin, sqrt

from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from flask_restful import Resource

from src.main import global_method as gm
from src.main import mongo as db

app = Flask(__name__)


class AvailableDrivers(Resource):
    def get(self, _id):
        # LOG INFO - get choferes disponibles
        token = request.headers['token']

        if gm.validate_token(token):
            # LOG INFO - correct token
            passenger = db.passengers.find_one({'_id': ObjectId(_id)})

            if not passenger:
                # LOG ERROR - _id inexistente
                return jsonify({"RESPONSE": "error"})

            repuesta = self._get_drivers_cercanos(passenger)

            return jsonify({"RESPONSE": repuesta, "token": token})
        else:
            # LOG ERROR - incorrect token
            return jsonify({"RESPONSE": "error"})

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
        for x in db.drivers.find({},{'_id':0 , 'lat': 1, 'lon': 1}):
            # print("conductor: ", x)
            if self._esta_cerca(passenger, x):
                cercanos.append(x)
        return cercanos
