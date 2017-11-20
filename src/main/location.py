from flask import Flask
from flask_restful import Resource

import src.main.constants.mongo_spec as db
from src.main.edit import validate_args

app = Flask(__name__)


def update_location(schema, collection, id): #Ver si conviene esto o herencia
    # validate_token(id)
    content = validate_args(schema)

    collection.update_one({'_id': id}, {
                            '$set': {
                                 'lon': content['lon'],
                                 'lat': content['lat']
                                 }
                            })


class LocatePassenger(Resource):
    schema = {
        'type': 'object',
        'properties': {
            'lat': {'type': 'number'},
            'lon': {'type': 'number'}
        },
        'required': ['lat', 'lon']
    }

    def put(self, id):
        update_location(self.schema, db.passengers, id)
        return 200


class LocateDriver(Resource):
    schema = {
        'type': 'object',
        'properties': {
            'lat': {'type': 'number'},
            'lon': {'type': 'number'}
        },
        'required': ['lat', 'lon']
    }

    def put(self, id):
        update_location(self.schema, db.drivers, id)
        return 200


