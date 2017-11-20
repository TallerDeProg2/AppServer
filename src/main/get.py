from flask import Flask, request
from flask_restful import Resource, abort
import requests
import logging
import src.main.mongo_spec as db


app = Flask(__name__)


class GetPassenger(Resource):
    def get(self, id):
        try:
            r = requests.get('direccionana/users' + id)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()


class GetDriver(Resource):
    def get(self, id):
        try:
            r = requests.get('direccionana/users' + id)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()


class GetCar(Resource):
    def get(self, id):
        try:
            r = requests.get('direccionana/users' + id + '/cars')
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)
        return r.json()
