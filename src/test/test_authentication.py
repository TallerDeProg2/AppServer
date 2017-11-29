import unittest
from nose.tools import assert_is_none, assert_list_equal
from unittest.mock import Mock, patch
from src.main.paths import app
import json


class TestAuthentication(unittest.TestCase):

    @patch('src.main.authentication.requests.post')
    @patch('src.main.global_method.encode_token')
    def test_adding_token_to_response(self, mock_encode, mock_post):
        input = {
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

        response_shared = {
            'user': {
                'username': 'pepe',
                'password': 'lalala',
                '_ref': '7284759248784',
                'cars': {},
                'fb': {
                        'userId': 'pepefb',
                        'authToken': '1234'
                    },
                'firstname': 'SOFIA',
                'lastname': 'argento',
                'country': 'argentina',
                'email': 'pepekpo@gmail.com',
                'birthdate': '27484',
                'id': '383948'
            }
        }

        output = [{
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
            'birthdate': '27484',
            'token': '74284297428',
            'id': '383948'
        }]

        mock_encode.return_value = '74284297428'

        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = response_shared

        app2 = app.test_client()
        response = app2.post('/validate', data=json.dumps(input), content_type='application/json')
        response_json = json.loads(response.get_data())

        assert_list_equal([response_json], output)
