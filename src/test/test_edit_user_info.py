from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_list_equal
from src.main.paths import app #Para pegarle a mi server sin tener que abrirlo manualmente
import requests
import json


@patch('src.main.global_method.validate_token')
@patch('src.main.edit.requests.get')
@patch('src.main.edit.requests.put')
def test_getting_user_when_response_is_ok(mock_put, mock_get, mock_validate_token):
    args = {
            'type': 'passenger',
            'username': 'pepe',
            'password': 'lalala',
            'fb': {
                    'userId': 'pepefb',
                    'authToken': '1234'
                },
            'firstname': 'SOFIA',
            'lastname': 'argento',
            'country': 'argentina',
            'email': 'pepekpo@gmail.com',
            'birthdate': '27484'
        }

    user = {
        'user': {
            '_ref': 5678,
            'username': 'pepe',
            'password': 'lalala',
            'cars': {},
            'fb': {
                    'userId': 'pepefb',
                    'authToken': '1234'
                },
            'firstname': 'juan',
            'lastname': 'argento',
            'country': 'argentina',
            'email': 'pepekpo@gmail.com',
            'birthdate': '27484'
        }
    }

    modified_user = {
        'user': {
            '_ref': 5678,
            'username': 'pepe',
            'password': 'lalala',
            'cars': {},
            'fb': {
                    'userId': 'pepefb',
                    'authToken': '1234'
                },
            'firstname': 'SOFIA',
            'lastname': 'argento',
            'country': 'argentina',
            'email': 'pepekpo@gmail.com',
            'birthdate': '27484'
        }
    }
    header = {'token': '838298'}

    mock_validate_token.return_value = True

    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = user

    mock_put.return_value = Mock(ok=True)
    mock_put.return_value.json.return_value = modified_user

    app2 = app.test_client()
    response = app2.put('/passengers/84748', data=json.dumps(args), headers=header,
                        content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], [modified_user['user']])


@patch('src.main.global_method.validate_token')
@patch('src.main.edit.requests.get')
@patch('src.main.edit.requests.put')
def test_getting_error_message_when_response_is_not_ok(mock_put, mock_get, mock_validate_token):
    args = {
            'username': 'pepe',
            'password': 'lalala',
            'fb': {
                    'userId': 'pepefb',
                    'authToken': '1234'
                },
            'firstname': 'SOFIA',
            'lastname': 'argento',
            'country': 'argentina',
            'email': 'pepekpo@gmail.com',
            'birthdate': '27484'
        }

    user = {
            '_ref': 5678,
            'username': 'pepe',
            'password': 'lalala',
            'fb': {
                    'userId': 'pepefb',
                    'authToken': '1234'
                },
            'firstname': 'juan',
            'lastname': 'argento',
            'country': 'argentina',
            'email': 'pepekpo@gmail.com',
            'birthdate': '27484'
        }
    header = {'token': '838298'}

    error_msg = [{
        'message': "Parámetros incorrectos",
        'status': 400
    }]

    mock_validate_token.return_value = True

    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = user

    mock_response = Mock()
    http_error = requests.exceptions.HTTPError()
    mock_response.raise_for_status.side_effect = http_error
    mock_response.status_code = 400

    mock_put.return_value = mock_response

    app2 = app.test_client()
    response = app2.put('/passengers/84748', data=json.dumps(args), headers=header,
                        content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], error_msg)

