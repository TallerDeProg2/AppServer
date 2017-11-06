from flask import Flask, request
from flask_restful import Resource, abort
import jsonschema as js
import logging
import requests
from pymongo import MongoClient
import googlemaps


app = Flask(__name__)

gmaps = googlemaps.Client(key='AIzaSyBwLajy8yXPyJ3QjXT-QcBqRDFSEj5_Acs')
client = MongoClient('mongodb://aybl:93731a@ds113775.mlab.com:13775/ubre_users', 27017)

db = client.ubre_users
passengers = db.passengers_test
drivers = db.drivers_test


class GetDirections(Resource):
    def get(self, id):
        # validate_token(token, id) #Devuelve T o F, loggear
        content = request.json
        try:
            js.validate(content, self.schema)
        except js.exceptions.ValidationError:
            logging.error('Argumentos ingresados inválidos')
            abort(400)

        origin = passengers.find({'id': id})
        payload = {}

        payload['lat'] = origin['lat']

        # r = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=content)
        directions_result = gmaps.directions("Sydney Town Hall",
                                             "Parramatta, NSW") #ver como meterle las coordenadas
