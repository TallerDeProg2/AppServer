import unittest
from unittest.mock import MagicMock, patch
from src.main.global_method import validate_token, encode_token
from src.main.query import AvailableDrivers
from src.test.mocks.NearestDrivers import nearestDrivers_result
from flask import Flask, current_app


app = Flask(__name__)


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/
# https://stackoverflow.com/questions/15753390/python-mock-requests-and-the-response


class TestQuery(unittest.TestCase):
    # @patch('src.main.mongo')
    # @patch('src.main.query.jsonify')
    # @patch('src.main.global_method.validate_token', return_value=False)
    # @patch('src.main.query.request')
    # def test_incorrect_token(self, mock_request, mock_gm, mock_json):
    #     with app.app_context():
    #         service = AvailableDrivers()
    #
    #         mock_request.headers.return_value = {"token": 1}
    #
    #         # VER ACA QUE ONDA PORQUE EN EL VALIDATE DE LA FUNCION LE TUVE QUE AGREGAR EL
    #         # ID SINO NO ME PASA Y ENTRA AL CODIGO MISTICAMENTE
    #         # mock_gm.validate_token.return_value = MagicMock()
    #         # NO ME ESTA MOCKEANDO
    #
    #         mock_json.return_value = MagicMock()
    #
    #         service.get("59dc0cbfc95bef1f4242b84c")
    #
    #         self.assertFalse(service._update_location.called)

    # @patch('src.main.query.jsonify')
    # @patch('src.main.global_method.validate_token', return_value=True)
    # @patch('src.main.query.request')
    # def test_correct_token(self, mock_request, mock_gm, mock_json):
    #     with app.app_context():
    #         service = AvailableDrivers()
    #
    #         mock_request.headers.return_value = {"token": 1}
    #
    #         service._update_location = MagicMock()
    #         service._get_drivers_cercanos = MagicMock()
    #         mock_json.return_value = MagicMock()
    #
    #         service.get("59dc0cbfc95bef1f4242b84c")

            # self.assertTrue(mock_gm.validate_tocken.called)

        # service = AvailableDrivers()
        #
        # mock_request.headers.return_value = {"token": 1}
        #
        # service.get(1)
        # service._update_locationt = MagicMock()
        # result = MagicMock(return_value=nearestDrivers_result)
        # self.assertEqual(service.get(1), {"RESPONSE": result, "token": encode_token(1)})
        # self.assertEqual(True, True)

    @patch('src.main.query.jsonify')
    @patch('src.main.query.request')
    def test_calculate_distance(self, mock_request, mock_json):
        service = AvailableDrivers()

        mock_request.args.get.return_value = {}
        passenger = {}

        service._calculate_distance(passenger)

        mock_json.jsonify.assert_called_with({"RESPONSE": "no tiene posicion de inicio"})

        # mock_request.args.get.return_value = {"lat": 0, "lon": 0}
        # passenger = {"lat": 0, "lon": 0}

    # # @patch('src.main.global_method.validate_token', return_value=False)
    # def test_calculateDistancecdeafsj(self, mock_get):
    #     service = AvailableDrivers()
    #     # service._get_actual_location = MagicMock(return_value='{lat:0,lon:0}')
    #     # service._update_locationt = MagicMock()
    #     # service._calculate_distance = MagicMock()
    #     # service._esta_cerca = MagicMock()
    #     # service._get_drivers_cercanos = MagicMock()
    #     # result = MagicMock(return_value=nearestDrivers_result)
    #     self.assertEqual(service.get(1), '{"RESPONSE": "error"}')
    #     self.assertEqual(True, True)
    #
    # # @patch('src.main.request', return_value={})
    # @patch('src.main.global_method.validate_token', return_value=True)
    # def test_calculateDistance(self, mock_get):
    #     service = AvailableDrivers()
    #     # service._get_actual_location = MagicMock(return_value='{lat:0,lon:0}')
    #     service._update_locationt = MagicMock()
    #     # service._calculate_distance = MagicMock()
    #     # service._esta_cerca = MagicMock()
    #     # service._get_drivers_cercanos = MagicMock()
    #     result = MagicMock(return_value=nearestDrivers_result)
    #     self.assertEqual(service.get(1), {"RESPONSE": result, "token": encode_token(1)})
    #     self.assertEqual(True, True)


#
#     def test_availableDrivers(self):
#         self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()


# def mocked_request_header():
#     class MockRequest:
#         # class Args:
#         #     def __init__(self):
#         #         self.args = {}
#         #
#         #     def get(self, value):
#         #         return self.args[value]
#
#         def __init__(self, header):
#             self.header = header
#             # self.args = self.Args()
#
#         def header(self):
#             return self.header
#
#         # def args(self):
#         #     return self.args
#
#     return MockRequest()

# This method will be used by the mock to replace requests.get
# def mocked_requests_get(*args, **kwargs):
#     class MockResponse:
#         def __init__(self, json_data, status_code):
#             self.json_data = json_data
#             self.status_code = status_code
#
#         def json(self):
#             return self.json_data
#
#     if args[0] == 'http://someurl.com/test.json':
#         return MockResponse({"key1": "value1"}, 200)
#     elif args[0] == 'http://someotherurl.com/anothertest.json':
#         return MockResponse({"key2": "value2"}, 200)
#
#     return MockResponse(None, 404)
#
# # Our test case class
# class MyGreatClassTestCase(unittest.TestCase):
#
#     # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
#     @mock.patch('requests.get', side_effect=mocked_requests_get)
#     def test_fetch(self, mock_get):
#         # Assert requests.get calls
#         mgc = MyGreatClass()
#         json_data = mgc.fetch_json('http://someurl.com/test.json')
#         self.assertEqual(json_data, {"key1": "value1"})
#         json_data = mgc.fetch_json('http://someotherurl.com/anothertest.json')
#         self.assertEqual(json_data, {"key2": "value2"})
#         json_data = mgc.fetch_json('http://nonexistenturl.com/cantfindme.json')
#         self.assertIsNone(json_data)
