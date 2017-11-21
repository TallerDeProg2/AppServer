# -*- coding: utf-8 -*-
import logging
import requests
from flask import Flask
from flask_restful import Api
from flask_restful import abort

from src.main import authentication, edit, query, directions, location

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
    }
}
# TODO generalizar los endpoints con plural o singular
api = Api(app, errors=errors)

api.add_resource(authentication.LogIn, '/validate')
api.add_resource(authentication.HelloWorld, '/hola')
api.add_resource(authentication.ByeWorld, '/chau')
api.add_resource(authentication.SignUpUser, '/users')

api.add_resource(edit.EditUser, '/passengers/<string:id>')
# api.add_resource(edit.EditUser, '/drivers/<string:id>')
api.add_resource(edit.EditCar, '/drivers/<string:id>/cars')
api.add_resource(edit.EditPayment, '/passengers/<string:id>/payment')

api.add_resource(location.LocatePassenger, '/passengers/<string:id>/location')
api.add_resource(location.LocateDriver, '/drivers/<string:id>/location')

api.add_resource(directions.GetDirections, '/passengers/<string:id>/directions')

api.add_resource(query.AvailableDrivers, '/passengers/<string:id>/drivers')
api.add_resource(query.AvailableTrips, '/drivers/<string:id>/trips')


# def getAppToken():
#     try:
#         r = requests.post('/servers/ping' + id, headers={'token': app.token})
#         r.raise_for_status()
#     except requests.exceptions.HTTPError:
#         logging.error('Conexión con el Shared dio error: ' + repr(r.status_code))
#         abort(r.status_code)
#     return r
