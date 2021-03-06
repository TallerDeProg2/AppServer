import logging
import googlemaps
import jsonschema as js
from flask import Flask, request
from flask_restful import Resource, abort
import src.main.constants.mongo_spec as db
import src.main.constants.schemas as sch
import src.main.global_method as gm

app = Flask(__name__)

gmaps = googlemaps.Client(key='AIzaSyBwLajy8yXPyJ3QjXT-QcBqRDFSEj5_Acs')


class GetDirections(Resource):
    schema = sch.location_schema

    def post(self, id):
        token = request.headers['token']
        if not gm.validate_token(token, id):
            logging.error('Token inválido')
            abort(401)
        content = request.json
        if not gm.validate_args(self.schema, content):
            abort(400)

        origindb = db.passengers.find_one({'_id': id})
        if origindb is None:
            logging.error('Id de usuario inexistente')
            abort(404)
        # origindb = {'lat': -34.5903345,
        #             'lon': -58.4161065}

        origin = str(origindb['lat']) + ',' + str(origindb['lon'])
        destiny = str(content['lat']) + ',' + str(content['lon'])
        directions = gmaps.directions(origin, destiny, alternatives=True)

        return {'routes': directions}, 201
