from flask import Flask, request
from flask_restful import Resource, abort
import jsonschema as js
import logging
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('mongodb://aybl:93731a@ds113775.mlab.com:13775/ubre_users', 27017)

db = client.ubre_users
passengers = db.passengers_test
drivers = db.drivers_test


class LocatePassenger(Resource):
    def post(self, id):
        # validate_token(token, id) #Devuelve T o F, loggear
        content = request.json
        try:
            js.validate(content, self.schema)
        except js.exceptions.ValidationError:
            logging.error('Argumentos ingresados inválidos')
            abort(400)

        passengers.update_one({'username': content['username']}, # ver si usar id o username
                              {'$set': {'long': content['long']},
                               '$set': {'lat': content['lat']}})
