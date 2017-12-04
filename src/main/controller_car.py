from flask import Flask, request
from flask_restful import Resource, abort
import logging
import src.main.constants.shared_server as ss
import src.main.constants.schemas as sch
import src.main.get as gets
import src.main.edit as edit
import src.main.post as posts
import src.main.global_method as gm

app = Flask(__name__)


class Car(Resource):
    def get(self, id):
        token = request.headers['token']
        if not gm.validate_token(token, id):
            logging.error('Token invalido')
            abort(401)
        service = gets.Get()
        car = service.get(ss.URL + '/users/' + repr(id) + '/cars')['car']
        car.pop('_ref') #TODO: Ver si ana SIEMPRE devuelve con ref
        return car

    def put(self, id):
        service = edit.Edit()
        car = service.put(id, ss.URL + '/users/' + repr(id) + '/cars', sch.car_schema)['car']
        car.pop('_ref')
        return car

    def post(self, id):
        token = request.headers['token']
        if not gm.validate_token(token, id):
            logging.error('Token invalido')
            abort(401)
        content = request.json
        if not gm.validate_args(sch.car_schema, content):
            abort(400)
        service = posts.Post()
        car = service.post(ss.URL + '/users/' + repr(id) + '/cars', content)['car']
        car.pop('_ref')
        return car
