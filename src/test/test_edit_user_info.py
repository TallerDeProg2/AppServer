from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_list_equal
from src.main import edit
from src.main.paths import app #Para pegarle a mi server sin tener que abrirlo manualmente
import requests
import json


@patch('src.main.edit.requests.get')
@patch('src.main.edit.requests.put')
def test_getting_user_when_response_is_ok(mock_put, mock_get):
    user = [{
        '_ref': 1234,
        'type': 'passenger',
        'username': 'pepe',
        'password': 'lalala',
        'firstName': 'juan',
        'lastName': 'argento',
        'country': 'argentina',
        'email': 'pepeargento@gmail.com',
        'birthdate': '154523'}]

    args = {'firstName': 'Sofia'}

    modified_user = [{
            '_ref': 1234,
            'type': 'passenger',
            'username': 'pepe',
            'password': 'lalala',
            'firstName': 'Sofia',
            'lastName': 'argento',
            'country': 'argentina',
            'email': 'pepeargento@gmail.com',
            'birthdate': '154523'}]

    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = user

    mock_put.return_value = Mock(ok=True)
    mock_put.return_value.json.return_value = modified_user

    # mock_put.side_effect = HttpError
    # mock_response = Mock()
    # http_error = requests.exceptions.HTTPError()
    # mock_response.raise_for_status.side_effect = http_error

    # mock_put.return_value = mock_response

    app2 = app.test_client()
    response = app2.put('/passengers/84748', data = json.dumps(args), content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal(response_json, modified_user)

