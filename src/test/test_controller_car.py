from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_list_equal
from src.main.paths import app #Para pegarle a mi server sin tener que abrirlo manualmente
import requests
import json


@patch('src.main.global_method.validate_token')
@patch('src.main.get.requests.get')
def test_getting_user_car_when_response_is_ok(mock_get, mock_validate_token):
    car_data = {
        'metadata': {

        },
        'car': {
            'brand': 'Fiat',
            'model': '7',
            'color': 'azul',
            'plate': '667 abc',
            'year': '1738',
            'status': 'new',
            'radio': 'yes',
            'airconditioner': True,
            '_ref': 'fjsisfjisjfsij'
        }
    }

    app_response = {
            'brand': 'Fiat',
            'model': '7',
            'color': 'azul',
            'plate': '667 abc',
            'year': '1738',
            'status': 'new',
            'radio': 'yes',
            'airconditioner': True
        }
    header = {'token': '838298'}

    mock_validate_token.return_value = True

    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = car_data

    app2 = app.test_client()
    response = app2.get('/drivers/84748/cars', headers=header)
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], [app_response])


@patch('src.main.global_method.validate_token')
@patch('src.main.post.requests.post')
def test_posting_user_car_when_response_is_ok(mock_post, mock_validate_token):
    car_data = {
        'metadata': {

        },
        'car': {
            'brand': 'Fiat',
            'model': '7',
            'color': 'azul',
            'plate': '667 abc',
            'year': '1738',
            'status': 'new',
            'radio': 'yes',
            'airconditioner': True,
            '_ref': 'fjsisfjisjfsij'
        }
    }

    input = {
            'brand': 'Fiat',
            'model': '7',
            'color': 'azul',
            'plate': '667 abc',
            'year': '1738',
            'status': 'new',
            'radio': 'yes',
            'airconditioner': True
        }

    app_response = {
            'brand': 'Fiat',
            'model': '7',
            'color': 'azul',
            'plate': '667 abc',
            'year': '1738',
            'status': 'new',
            'radio': 'yes',
            'airconditioner': True
        }
    header = {'token': '838298'}

    mock_validate_token.return_value = True

    mock_post.return_value = Mock(ok=True)
    mock_post.return_value.json.return_value = car_data

    app2 = app.test_client()
    response = app2.post('/drivers/84748/cars', data=json.dumps(input), headers=header,
                        content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], [app_response])