from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_list_equal
from src.main.paths import app #Para pegarle a mi server sin tener que abrirlo manualmente
import requests
import json


@patch('src.main.directions.gmaps')
@patch('src.main.constants.mongo_spec.passengers')
@patch('src.main.global_method.validate_token')
def test_getting_directions(mock_validate_token, mock_passengers, mock_directions):
    input = {
            'lat': 47.2737,
            'lon': 28.284
        }

    passenger = {
            "_id": 1,
            "lat": 1,
            "lon": 1
        }

    directions_response = {
                'directions': 'Lots of directions'
            }
    expected_response = {
                'routes': directions_response
            }

    header = {'token': '838298'}

    mock_validate_token.return_value = True

    mock_passengers.find_one.return_value = passenger
    mock_directions.directions.return_value = directions_response

    app2 = app.test_client()
    response = app2.post('/passengers/1/directions', data=json.dumps(input), headers=header,
                        content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], [expected_response])