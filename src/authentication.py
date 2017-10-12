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
    def post(self):
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('facebookAuthToken', type=str, required=True)
        args = parser.parse_args(strict=True)

        try:
            r = requests.post('direccionana/users/validate', json=args)
            r.raise_for_status()
        except requests.exception.HTTPError:
            #Ver si mandar error a alan o se manda solo
        #Crear token
        #Crear usuario en database, con formato de db
        coll.insert_one(r.json())
        #return r.json()
        return args


class SignUp(Resource):
    fields = ['username', 'password', 'fb.userID', 'fb.authToken', 'firstName', 'lastName',
              'country', 'email', 'birthdate']

    def post(self):
        for i in self.fields[:]:
            parser.add_argument(i, type=str, required=True)

        args = parser.parse_args(strict=True)

        r = requests.post('direccionana/users', json=args)
        return r.json()