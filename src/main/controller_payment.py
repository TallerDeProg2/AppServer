from flask import Flask
from flask_restful import Resource, reqparse, abort
import src.main.constants.shared_server as ss
import src.main.constants.schemas as sch
import src.main.get as gets
import src.main.edit as edit

app = Flask(__name__)


class Payment(Resource):
    def get(self, id):
        service = gets.Get()
        return service.get(ss.URL + '/users/' + id + '/payment')

    def put(self, id):
        service = edit.Edit()
        return service.put(id, ss.URL + '/users/' + id + '/payment', sch.payment_schema)