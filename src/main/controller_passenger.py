from flask import Flask
from flask_restful import Resource, reqparse, abort
import requests
import src.main.constants.shared_server as ss
import src.main.constants.schemas as sch
import logging
import src.main.edit as edit
import src.main.authentication as auth
import src.main.get as gets

app = Flask(__name__)


class Passenger(Resource):
    def get(self, id):
        service = gets.Get()
        return service.get(ss.URL + '/users/' + id)

    def put(self, id):
        service = edit.Edit()
        return service.put(id, ss.URL + '/users/' + id, sch.user_full_schema)
