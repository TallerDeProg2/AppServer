from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_list_equal
from src.main.paths import app #Para pegarle a mi server sin tener que abrirlo manualmente
import requests
import json


@patch('src.main.constants.mongo_spec.drivers')
@patch('src.main.constants.mongo_spec.trips')
@patch('src.main.global_method.validate_token')
@patch('src.main.match.requests.get')
@patch('src.main.match.requests.post')
def test_ending_trip_when_response_is_ok(mock_post, mock_get, mock_validate_token, mock_trips, mock_drivers):
    args = {
            'paymethod': 'card'
        }

    trip = {
        "_id": 20,
        "passenger": 22,
        "driver": 4874,
        "start": {
            "street": "Av. Pres. Roque Sáenz Peña 999, C1035AAE CABA, Argentina",
            "location": {
                "lat": -34.6038333,
                "lon": -58.3815047
            }
        },
        "end": {
            "street": "Gral. Lucio Norberto Mansilla 3701-3721, C1425BPY CABA, Argentina",
            "location": {
                "lat": -34.5901404,
                "lon": -58.41590160000001
            }
        },
        "totalTime": 422796,
        "waitTime": 130833,
        "travelTime": 291963,
        "distance": 78393,
        "startTime": "2017-12-02 11:40:43",
        "status": "finished",
        "cost": {
            "currency": "ARS",
            "value": 2635760
        }
    }

    card = {
        'metadata': {'version': '1.0'},
        'card': {
            'ccvv': '11111',
            'type': 'Visa',
            'method': 'card',
            'number': '123456789123',
            'expiration_year': '20',
            'expiration_month': '12'}
    }

    cost = {
        'metadata': {'version': '1.0'},
        'cost': {
            'currency': 'ARS',
            'value': 3043890}
    }

    expected_response = {
            'currency': 'ARS',
            'value': 3043890
    }

    header = {'token': '838298'}

    mock_validate_token.return_value = True

    mock_trips.find_one.return_value = trip
    mock_trips.update_one.return_value = None
    mock_drivers.update_one.return_value = None

    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = card

    mock_response = Mock()
    mock_response.status_code = 200

    mock_post.return_value = Mock(ok=True)
    mock_post.status_code = 200
    mock_post.return_value.json.return_value = cost

    app2 = app.test_client()
    response = app2.post('/trips/20/end', data=json.dumps(args), headers=header,
                        content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], [expected_response])