from flask import Flask, request
from flask_restful import Resource, abort
import jsonschema as js
import logging
import src.main.mongo_spec as db
import googlemaps


app = Flask(__name__)

gmaps = googlemaps.Client(key='AIzaSyBwLajy8yXPyJ3QjXT-QcBqRDFSEj5_Acs')


class GetDirections(Resource):
    schema = {
        'type': 'object',
        'properties': {
            'lat': {'type': 'number'},
            'long': {'type': 'number'},
            'token': {'type': 'integer'}
        },
        'required': ['lat', 'long', 'token']
    }

    def put(self, id):
        # validate_token(token, id) #Devuelve T o F, loggear
        content = request.json
        try:
            js.validate(content, self.schema)
        except js.exceptions.ValidationError:
            logging.error('Argumentos ingresados inválidos')
            abort(400)

        origindb = db.passengers.find({'_id': id})
        # origindb = {'lat': -34.5903345,
        #             'long': -58.4161065}

        origin = str(origindb['lat']) + ',' + str(origindb['long'])
        destiny = str(content['lat']) + ',' + str(content['long'])
        directions = gmaps.directions(origin, destiny)

        return directions
