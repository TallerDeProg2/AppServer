from src.main import config
import jwt
import datetime
from flask import request
import jsonschema as js
import logging
from flask_restful import abort
from pyfcm import FCMNotification


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


def validate_args(schema, content):
    ok = True
    try:
        js.validate(content, schema)
    except js.exceptions.ValidationError:
        logging.error('Argumentos ingresados inválidos')
        ok = False

    return ok


def build_response(r): #TODO: Meterle el fb o pedirle a ana q lo mande
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


def push_notif(id, message_title, message_body):
    api_keys = 'AAAAaxCakgY:APA91bG4JlqQn6YhGAoPck1_moeHW4PxUWiPxnjEmxqfbVLTCVk7Wfn6fOq7AR7b_zPBF0oR9ln-d1maLH5ZoqbFea0eEl0O10RHUYyljyztqkwJEq46kZwVgKgt377PwVH00pjR87i4'

    push_service = FCMNotification(api_key=api_keys)
    push_service.notify_topic_subscribers(topic_name=str(id), message_title=message_title,
                                          message_body=message_body)

