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


class Passenger(Resource):
    def get(self, id):
        token = request.headers['token']
        if not gm.validate_token(token, id):
            logging.error('Token invalido')
            abort(401)
        service = gets.Get()
        r = service.get(ss.URL + '/users/' + repr(id))
        return gm.build_response(r)

    def put(self, id):
        service = edit.Edit()
        r = service.put(id, ss.URL + '/users/' + repr(id), sch.user_full_schema)
        return gm.build_response(r)
