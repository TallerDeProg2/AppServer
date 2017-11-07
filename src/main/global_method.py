from src.main import config
import jwt
import datetime


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
