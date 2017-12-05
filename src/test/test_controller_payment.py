from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_list_equal
from src.main.paths import app #Para pegarle a mi server sin tener que abrirlo manualmente
import requests
import json


@patch('src.main.global_method.validate_token')
@patch('src.main.get.requests.get')
def test_getting_user_card_when_response_is_ok(mock_get, mock_validate_token):
    card_data = {
        'metadata': {

        },
        'card': {
            'ccvv': '274827484',
            'expiration_month': '12',
            'expiration_year': '1738',
            'method': 'card',
            'number': '27484277',
            'type': 'visa'
        }
    }

    app_response = {
            'ccvv': '274827484',
            'expiration_month': '12',
            'expiration_year': '1738',
            'method': 'card',
            'number': '27484277',
            'type': 'visa'
        }
    header = {'token': '838298'}

    mock_validate_token.return_value = True

    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = card_data

    app2 = app.test_client()
    response = app2.get('/passengers/84748/card', headers=header)
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], [app_response])


@patch('src.main.global_method.validate_token')
@patch('src.main.post.requests.post')
def test_posting_user_card_when_response_is_ok(mock_post, mock_validate_token):
    card_data = {
        'metadata': {

        },
        'card': {
            'ccvv': '274827484',
            'expiration_month': '12',
            'expiration_year': '1738',
            'method': 'card',
            'number': '27484277',
            'type': 'visa'
        }
    }

    input = {
        'ccvv': '274827484',
        'expiration_month': '12',
        'expiration_year': '1738',
        'method': 'card',
        'number': '27484277',
        'type': 'visa'
    }

    app_response = {
            'ccvv': '274827484',
            'expiration_month': '12',
            'expiration_year': '1738',
            'method': 'card',
            'number': '27484277',
            'type': 'visa'
        }
    header = {'token': '838298'}

    mock_validate_token.return_value = True

    mock_post.return_value = Mock(ok=True)
    mock_post.return_value.json.return_value = card_data

    app2 = app.test_client()
    response = app2.post('/passengers/84748/card', data=json.dumps(input), headers=header,
                        content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], [app_response])


@patch('src.main.global_method.validate_token')
@patch('src.main.get.requests.get')
def test_getting_error_message_when_response_is_not_ok(mock_get, mock_validate_token):
    header = {'token': '838298'}

    error_msg = [{
        'message': "Parámetros incorrectos",
        'status': 400
    }]

    mock_validate_token.return_value = True

    mock_response = Mock()
    http_error = requests.exceptions.HTTPError()
    mock_response.raise_for_status.side_effect = http_error
    mock_response.status_code = 400

    mock_get.return_value = mock_response

    app2 = app.test_client()
    response = app2.get('/passengers/84748/card', headers=header)
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], error_msg)


@patch('src.main.global_method.validate_token')
@patch('src.main.post.requests.post')
def test_getting_error_message_when_response_is_not_ok(mock_post, mock_validate_token):
    input = {
        'ccvv': '274827484',
        'expiration_month': '12',
        'expiration_year': '1738',
        'method': 'card',
        'number': '27484277',
        'type': 'visa'
    }
    header = {'token': '838298'}

    error_msg = [{
        'message': "Parámetros incorrectos",
        'status': 400
    }]

    mock_validate_token.return_value = True

    mock_response = Mock()
    http_error = requests.exceptions.HTTPError()
    mock_response.raise_for_status.side_effect = http_error
    mock_response.status_code = 400

    mock_post.return_value = mock_response

    app2 = app.test_client()
    response = app2.post('/passengers/84748/card', data=json.dumps(input), headers=header,
                        content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], error_msg)