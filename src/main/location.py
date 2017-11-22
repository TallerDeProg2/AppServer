from flask import Flask
from flask_restful import Resource
import src.main.constants.schemas as sch
import src.main.constants.mongo_spec as db
import src.main.global_method as gm

app = Flask(__name__)


def update_location(schema, collection, id):
    gm.check_token(id)
    content = gm.validate_args(schema)

    collection.update_one({'_id': id}, {
                            '$set': {
                                 'lon': content['lon'],
                                 'lat': content['lat']
                                 }
                            })


class LocatePassenger(Resource):
    def put(self, id):
        update_location(sch.location_schema, db.passengers, id)
        return 200


class LocateDriver(Resource):
    def put(self, id):
        update_location(sch.location_schema, db.drivers, id)
        return 200


