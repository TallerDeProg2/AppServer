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
    schema = {
        'type': 'object',
        'properties': {
            'lat': {'type': 'number'},
            'lon': {'type': 'number'},
            'token': {'type': 'integer'}
        },
        'required': ['lat', 'lon', 'token']
    }

    def put(self, id):
        # validate_token(token, id) #Devuelve T o F, loggear
        content = request.json
        try:
            js.validate(content, self.schema)
        except js.exceptions.ValidationError:
            logging.error('Argumentos ingresados inválidos')
            abort(400)

        # origindb = passengers.find({'id': id})
        origindb = {'lat': -34.5903345,
                    'lon': -58.4161065}

        origin = str(origindb['lat']) + ',' + str(origindb['lon'])
        destiny = str(content['lat']) + ',' + str(content['lon'])
        # r = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=content)
        directions = gmaps.directions(origin, destiny)

        return directions
