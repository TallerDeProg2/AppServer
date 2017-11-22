from flask import Flask
from flask_restful import Resource, reqparse, abort
import requests
import src.main.constants.shared_server as ss
import src.main.constants.schemas as sch
import logging
import src.main.edit as edit
import src.main.authentication as auth

app = Flask(__name__)


class Passenger(Resource):
    def get(self, id):
        try:
            r = requests.get(ss.URL + '/users/' + id)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
            abort(r.status_code)

    def put(self, id):
        service = edit.Edit()
        return service.put(id, ss.URL + '/users/' + id, sch.user_full_schema)
