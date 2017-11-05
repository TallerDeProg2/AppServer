from src.main import authentication
from src.main import edit
from flask import Flask
from flask_restful import Api
import logging

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    filename='ubreLogs.log',
                    filemode='w')

errors = {
    'BadRequest': {
        'message': "Parámetros incorrectos",
        'status': 400
    },
    'NotFound': {
        'message': "Recurso inexistente",
        'status': 404
    },
    'InternalServerError': {
        'message': "Error inesperado",
        'status': 500
    }
}

api = Api(app, errors=errors)

api.add_resource(authentication.LogIn, '/')
api.add_resource(authentication.HelloWorld, '/hola')
api.add_resource(edit.EditUser, '/passengers/<string:id>')
api.add_resource(authentication.SignUpPassenger, '/passengers')
api.add_resource(authentication.SignUpDriver, '/drivers')