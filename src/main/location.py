from flask import Flask
from flask_restful import Resource
from pymongo import MongoClient
from src.main.edit import validate_token, validate_args


app = Flask(__name__)

client = MongoClient('mongodb://sofafafa:sofafafa1@ds141098.mlab.com:41098/ubre')
db = client['ubre']
drivers_db = db['drivers_test']
passengers_db = db['passengers_test']


def update_location(schema, collection, id): #Ver si conviene esto o herencia
    # validate_token(id)
    content = validate_args(schema)

    collection.update_one({'_id': id},
                             {'$set': {
                                 'long': content['long'],
                                 'lat': content['lat']
                             }})


class LocatePassenger(Resource):
    schema = {
        'type': 'object',
        'properties': {
            'lat': {'type': 'number'},
            'long': {'type': 'number'}
        },
        'required': ['lat', 'long']
    }

    def put(self, id):
        update_location(self.schema, passengers_db, id)
        return 200


class LocateDriver(Resource):
    schema = {
        'type': 'object',
        'properties': {
            'lat': {'type': 'number'},
            'long': {'type': 'number'}
        },
        'required': ['lat', 'long']
    }

    def put(self, id):
        update_location(self.schema, drivers_db, id)
        return 200


