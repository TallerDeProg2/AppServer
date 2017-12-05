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


class PassengerPayment(Resource): #TODO: Ver que me devuelve ana y crear respuesta acorde
    def get(self, id):
        token = request.headers['token']
        if not gm.validate_token(token, id):
            logging.error('Token invalido')
            abort(401)
        service = gets.Get()
        return service.get(ss.URL + '/users/' + repr(id) + '/card')['card']

    def put(self, id):
        service = edit.Edit()
        return service.put(id, ss.URL + '/users/' + repr(id) + '/card', sch.payment_schema)['card']

    def post(self, id):
        content = request.json
        if not gm.validate_args(sch.payment_schema, content):
            abort(400)
        service = posts.Post()
        return service.post(ss.URL + '/users/' + repr(id) + '/card', content)['card']


class DriverPayment(Resource):
    def get(self, id):
        token = request.headers['token']
        if not gm.validate_token(token, id):
            logging.error('Token invalido')
            abort(401)
        service = gets.Get()
        return service.get(ss.URL + '/users/' + repr(id) + '/card')['card']

    def put(self, id):
        service = edit.Edit()
        return service.put(id, ss.URL + '/users/' + repr(id) + '/card', sch.payment_schema)['card']

    def post(self, id):
        content = request.json
        if not gm.validate_args(sch.payment_schema, content):
            abort(400)
        service = posts.Post()
        return service.post(ss.URL + '/users/' + repr(id) + '/card', content)['card']