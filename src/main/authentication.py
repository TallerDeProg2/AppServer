from flask import Flask
from flask_restful import Resource, reqparse
import requests
from pymongo import MongoClient

app = Flask(__name__)
parser = reqparse.RequestParser()

client = MongoClient('localhost', 27017)
db = client.baseprueba
coll = db.baseprueba


class HelloWorld(Resource):
    def get(self):
        return "Hola"


class LogIn(Resource):
    """Permite loggear un usuario"""
    def post(self):
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('facebookAuthToken', type=str, required=True)
        args = parser.parse_args(strict=True)

        # try:
        r = requests.post('direccionana/users/validate', json=args)
        r.raise_for_status()
        # except requests.exception.HTTPError:
            #Ver si mandar error a alan o se manda solo
        #Crear token
        #token = encode_token(id)
        #Crear usuario en database, con formato de db
        coll.insert_one('_id: 74748548, token: 8725889227')
        #return r.json()
        return args


class SignUpUser(Resource):
    # fields = ['username', 'password', 'fb.userID', 'fb.authToken', 'firstName', 'lastName',
    #           'country', 'email', 'birthdate']

    def post(self):
        """Permite registrar un usuario"""
        for i in self.fields[:]:
            parser.add_argument(i, type=str, required=True)

        args = parser.parse_args(strict=True)

        # try:
        #     r = requests.post('direccionana/users', json=args)
        #     r.raise_for_status()
        # except requests.exception.HTTPError:
            #Ver si mandar error a alan o se manda solo
        # return r.json(), 200
        return args

class SignUpPassenger(SignUpUser):
    # fields = ['username', 'password', 'fb.userID', 'fb.authToken', 'firstName', 'lastName',
    #           'country', 'email', 'birthdate']
    fields = ['username', 'password']

class SignUpDriver(SignUpUser):
    # fields = ['username', 'password', 'fb.userID', 'fb.authToken', 'firstName', 'lastName',
    #           'country', 'email', 'birthdate']
    fields = ['username', 'password']