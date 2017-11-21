import logging
import googlemaps
import jsonschema as js
from flask import Flask, request
from flask_restful import Resource, abort
import src.main.constants.mongo_spec as db
import src.main.constants.schemas as sch

app = Flask(__name__)

gmaps = googlemaps.Client(key='AIzaSyBwLajy8yXPyJ3QjXT-QcBqRDFSEj5_Acs')


class GetDirections(Resource):
    schema = sch.location_schema

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
        #             'lon': -58.4161065}

        origin = str(origindb['lat']) + ',' + str(origindb['lon'])
        destiny = str(content['lat']) + ',' + str(content['lon'])
        directions = gmaps.directions(origin, destiny)

        return directions
