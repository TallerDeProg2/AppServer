# -*- coding: utf-8 -*-

import logging
import requests

from src.main import authentication, query, directions, location, controller_passenger, controller_car, controller_payment, controller_driver

from flask import Flask
from flask_restful import Api
from flask_restful import abort

from src.main import authentication, edit, query, directions, location, match

app = Flask(__name__)
app.config["token"] = "servercito-token"

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
    },
    'Conflict': {
        'message': "Solicitud no pudo ser procesada por conflicto de recursos",
        'status': 409
    }
}
# TODO generalizar los endpoints con plural o singular
api = Api(app, errors=errors)

api.add_resource(authentication.LogIn, '/validate')
api.add_resource(authentication.HelloWorld, '/hola')
api.add_resource(authentication.ByeWorld, '/chau')
api.add_resource(authentication.SignUpUser, '/users')


api.add_resource(controller_passenger.Passenger, '/passengers/<int:id>')
api.add_resource(controller_driver.Driver, '/drivers/<int:id>')
api.add_resource(controller_car.Car, '/drivers/<int:id>/cars')
api.add_resource(controller_payment.Payment, '/passengers/<int:id>/payment')


api.add_resource(location.LocatePassenger, '/passengers/<int:id>/location')
api.add_resource(location.LocateDriver, '/drivers/<int:id>/location')

api.add_resource(directions.GetDirections, '/passengers/<int:id>/directions')

api.add_resource(query.AvailableDrivers, '/passengers/<string:id>/drivers')
api.add_resource(query.AvailableTrips, '/drivers/<string:id>/trips')

api.add_resource(match.TripRequest, '/passengers/<int:id>/trips/request')
api.add_resource(match.TripEstimate, '/trips/estimate')

