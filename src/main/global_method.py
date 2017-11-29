from src.main import config
import jwt
import datetime
from flask import request
import jsonschema as js
import logging
from flask_restful import abort


def encode_token(user_id):
    """
    Generates the Token
    :return: string
    """
    if user_id:
        # LOG INFO -generacion de token-
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=100, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
        return token.decode("utf-8", "ignore")
    else:
        # LOG ERROR -no id-
        return None


def decode_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, config.SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def validate_token(token, user_id=None):
    decoded_token = decode_token(token)
    if decoded_token:
        if not user_id:
            return True
        else:
            return decoded_token == user_id
    return False


def validate_args(schema):
    content = request.json   # Ver si esto bien o mal
    try:
        js.validate(content, schema)
    except js.exceptions.ValidationError:
        logging.error('Argumentos ingresados inválidos')
        abort(400)

    return content


def check_token(id):
    token = request.headers['token']  # Ver si esto bien o mal
    if not validate_token(token, id):
        logging.error('Token inválido')
        abort(401)


def build_response(r): #Meterle el fb o pedirle a ana q lo mande
    """
        Generates a suitable response for the client
        :param json:
        :return: json
    """
    response = r['user']
    # response['token'] = token
    response.pop('_ref')
    response.pop('cars')

    return response

