from flask import Flask
from flask_restful import Resource, reqparse
import requests

app = Flask(__name__)
parser = reqparse.RequestParser()


class EditPassenger(Resource):
    fields = ['username', 'password', 'fb.userID', 'fb.authToken', 'firstName', 'lastName',
              'country', 'email', 'birthdate']

    def put(self):
        r = requests.get('direccionana/users/passenger_id')
        r = r.json()
        # r = {
        #     '_ref': 1234,
        #     'type': 'passenger',
        #     'username': 'pepe',
        #     'password': 'lalala',
        #     'firstName': 'juan',
        #     'lastName': 'argento',
        #     'country': 'argentina',
        #     'email': 'pepeargento@gmail.com',
        #     'birthdate': '154523'
        # }
        for i in self.fields[:]:
            parser.add_argument(i, type=str)

        args = parser.parse_args(strict=True)

        for i in self.fields[:]:
            r[i] = args[i]

        q = requests.put('direccionana/users/passenger_id', json=r)
        try:
            r = requests.put('direccionana/users/passenger_id', json=r)
            r.raise_for_status()
        except requests.exception.HTTPError:
            if r.status_code == 409:
                """Valor de _ref desactualizado"""
                return self.put(passenger_id)
        return q.json()
        # return r
