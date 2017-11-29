from flask import Flask
from flask_restful import Resource
import src.main.constants.shared_server as ss
import src.main.constants.schemas as sch
import src.main.edit as edit
import src.main.get as gets

app = Flask(__name__)


class Driver(Resource):
    def get(self, id):
        service = gets.Get() #TODO: Validar que devuelva driver y no passenger
        return service.get(ss.URL + '/users/' + id)

    def put(self, id):
        service = edit.Edit()
        return service.put(id, ss.URL + '/users/' + id, sch.user_full_schema)
