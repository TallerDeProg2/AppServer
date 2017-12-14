from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_list_equal
from src.main.paths import app
import requests
import json


@patch('src.main.constants.mongo_spec.passengers')
@patch('src.main.global_method.validate_token')
def test_save_passengers_location(mock_validate_token, mock_passengers):
    input = {
            'lat': 47.2737,
            'lon': 28.284
        }

    header = {'token': '838298'}

    mock_validate_token.return_value = True

    mock_passengers.update_one.return_value = None

    app2 = app.test_client()
    response = app2.put('/passengers/1/location', data=json.dumps(input), headers=header,
                        content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], [200])


@patch('src.main.constants.mongo_spec.drivers')
@patch('src.main.global_method.validate_token')
def test_save_drivers_location(mock_validate_token, mock_drivers):
    input = {
            'lat': 47.2737,
            'lon': 28.284
        }

    header = {'token': '838298'}

    mock_validate_token.return_value = True

    mock_drivers.update_one.return_value = None

    app2 = app.test_client()
    response = app2.put('/drivers/1/location', data=json.dumps(input), headers=header,
                        content_type='application/json')
    response_json = json.loads(response.get_data())

    assert_list_equal([response_json], [200])