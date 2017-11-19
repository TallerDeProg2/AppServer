from flask import Flask, request
from flask_restful import Resource, abort
from pymongo import MongoClient
from src.main.edit import validate_token, validate_args


app = Flask(__name__)

client = MongoClient('mongodb://sofafafa:sofafafa1@ds141098.mlab.com:41098/ubre')
db = client['ubre']
drivers_db = db['drivers_test']
passengers_db = db['passengers_test']


class LocatePassenger(Resource):
    schema = {
        'type': 'object',
        'properties': {
            'lat': {'type': 'number'},
            'long': {'type': 'number'}
        },
        'required': ['lat', 'long']
    }

    def post(self, id):
        # validate_token(id)
        content = validate_args(self.schema)

        passengers_db.update_one({'_id': id},
                                 {'$set': {
                                     'long': content['long'],
                                     'lat': content['lat']
                                 }})
        return 200
