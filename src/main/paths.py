# -*- coding: utf-8 -*-
from src.main import authentication, edit, query, directions, location
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
    },
    'Unauthorized': {
        'message': "No autorizado",
        'status': 401
    }
}
#TODO generalizar los endpoints con plural o singular
api = Api(app, errors=errors)

api.add_resource(authentication.LogIn, '/')
api.add_resource(authentication.HelloWorld, '/hola')
api.add_resource(authentication.ByeWorld, '/chau')
api.add_resource(authentication.SignUpUser, '/users')

api.add_resource(edit.EditUser, '/passengers/<string:id>')
api.add_resource(edit.EditCar, '/driver/<string:id>/cars')
api.add_resource(edit.EditPayment, '/passengers/<string:id>/payment')

api.add_resource(location.LocatePassenger, '/passengers/<string:id>/location')
api.add_resource(location.LocateDriver, '/drivers/<string:id>/location')

api.add_resource(directions.GetDirections, '/passengers/<string:id>/directions')

api.add_resource(query.AvailableDrivers, '/passengers/<string:id>/drivers')
api.add_resource(query.AvailableTrips, '/drivers/<string:id>/trips')
