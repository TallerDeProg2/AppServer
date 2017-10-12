import authentication
import edit
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

errors = {
    'MissingArguments': {
        'message': "Parámetros faltantes",
        'status': 400
    },
    'ResourceDoesNotExist': {
        'message': "Recurso inexistente",
        'status': 404
    },
    'UnexpectedError': {
        'message': "Error inesperado",
        'status': 500
    }
}

api = Api(app, errors=errors)

api.add_resource(authentication.LogIn, '/')
api.add_resource(authentication.HelloWorld, '/hola')
# api.add_resource(edit.EditPassenger, '/passengers/<string:passenger_id>')
api.add_resource(edit.EditPassenger, '/passengers')