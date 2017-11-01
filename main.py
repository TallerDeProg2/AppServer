from math import radians, cos, sin, asin, sqrt, inf
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from bson.objectid import ObjectId
from pymongo import MongoClient
from src import global_method as gm

app = Flask(__name__)
api = Api(app)

client = MongoClient('localhost', 27017)

db = client.passengers_test
passengers = db.passengers_test
drivers = db.drivers_test


# class Pruebas(Resource):
#     # def get(self):
#     #     nom = request.args.get('Nombre')
#     #     query = [{"Nombre": x["Nombre"], "Apellido": x["Apellido"]} for x in passengers.find({"Nombre": nom})]
#     #     return jsonify({"RESPONSE": query})
#
# CODIGO PARA GENERAR LOS TOKEN A VECES ME DABAN DISTINTOS CON SOLO HARCODERA EL GM EN 'sub': EN VEZ DE 'sub': user_id
#     def put(self):
#         self._actualizar_tokens()
#         return jsonify({"RESPONSE": 'se actualizaron los tokens segun id'})
#
#     def _actualizar_tokens(self):
#         """SOLO PARA ACTUALIZAR LA BASE CON EL TOKEN SEGUN NUESTRO ID Y UNA CLAVE"""
#         cour = drivers.find()
#         i = 0
#         for x in cour:
#             i += 1
#             user_id = x['_id']
#             token = gm.encode_token(str(i))
#             a = drivers.find_one_and_update({"_id": ObjectId(user_id)}, {'$set': {'token': token}})
#             s = gm.decode_token(token)
#             pass

#api.add_resource(Pruebas, '/')


# class User(Resource):
#     def get(self, todo_id):
#         query = [{"token": x["token"]} for x in passengers.find({"_id": todo_id})]
#         return jsonify({"RESPONSE": query})
#
#     def put(self, todo_id):
#         args = request.get_json()
#         if not args:
#             return jsonify({"RESPONSE": "La remil mierda"})
#         else:
#             nom = args.get('Nombre')
#             chorongp = passengers.find_one_and_update({"Nombre": todo_id}, {'$set': {"Nombre": nom}})
#             return jsonify({"RESPONSE": nom})
#
#
# api.add_resource(User, '/<string:todo_id>')


class AvailableDrivers(Resource):
    def get(self, _id):
        # LOG INFO - get choferes disponibles
        token = request.headers['token']

        if gm.validate_token(token):
            # LOG INFO - correct token
            passenger = passengers.find_one({'_id': ObjectId(_id)})

            self._update_location(passenger)
            repuesta = self._get_drivers_cercanos(passenger)

            return jsonify({"RESPONSE": repuesta, "token": token})
        else:
            # LOG ERROR - incorrect toke
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
        lat, lon = self._get_actual_location(passenger)
        passengers.find_one_and_update({"_id": passenger['_id']},
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
        for x in drivers.find():
            if self._esta_cerca(passenger, x['lon'], x['lat']):
                cercanos.append({'lon': x['lon'], 'lat': x['lat']})
        return cercanos


api.add_resource(AvailableDrivers, '/passenger/<string:_id>/drivers')

if __name__ == '__main__':
    # if os.environ[]
    app.run(debug=True)
