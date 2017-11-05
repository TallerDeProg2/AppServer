from flask import Flask
from flask_restful import Resource, reqparse
import requests

app = Flask(__name__)
parser = reqparse.RequestParser()


class EditUser(Resource):
    # fields = ['username', 'password', 'fb.userID', 'fb.authToken', 'firstName', 'lastName',
    #           'country', 'email', 'birthdate']

    def put(self, id):
        """Permite modificar un usuario"""
        #validate_token(token, id) #Devuelve T o F, loggear
        r = requests.get('direccionana/users/' + id)
        r = r.json()[0] #fixear
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

        print(r)

        for i in self.fields[:]:
            r[i] = args[i]

        # q = requests.put('direccionana/users/' + id, json=r)
        try:
            r = requests.put('direccionana/users/' + id, json=r)
            r.raise_for_status()
        except requests.exception.HTTPError:
            if r.status_code == 409:
                """Valor de _ref desactualizado"""
                # return self.put(id) #no necesario hacer esto, simplemente devolver a alan el codigo de error y q ellos se encarguen
                return 1
        return r.json()
        # return r


class EditPassenger(EditUser):
    fields = ['username', 'password', 'fb.userID', 'fb.authToken', 'firstName', 'lastName',
              'country', 'email', 'birthdate']


class EditDriver(EditUser):
    fields = ['username', 'password', 'fb.userID', 'fb.authToken', 'firstName', 'lastName',
              'country', 'email', 'birthdate']
