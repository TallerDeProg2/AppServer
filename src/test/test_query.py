import unittest

import requests
from flask import Flask
from mock import patch, MagicMock

from src.main.query import AvailableDrivers, AvailableTrips

app = Flask(__name__)
app.config['TESTING'] = True

drivers = [{'id': 1, 'lat': 10, 'lon': 14},
           {'id': 4, 'lat': 0, 'lon': 34},
           {'id': 5, 'lat': 10, 'lon': 5},
           {'id': 10, 'lat': 22, 'lon': 10}]

passenger = {'id': 2, 'lat': 0, 'lon': 0}

driver = {'id': 1, 'lat': 0, 'lon': 0}

trips = [
    {'id': 1, 'passenger': 45, 'origin': {'lat': 0, 'lon': 0}, 'destination': {'lat': 3, 'lon': 5}, 'directions': {}},
    {'id': 2, 'passenger': 4, 'origin': {'lat': 0, 'lon': 0}, 'destination': {'lat': 1, 'lon': 2}, 'directions': {}},
    {'id': 3, 'passenger': 15, 'origin': {'lat': 0, 'lon': 0}, 'destination': {'lat': 0, 'lon': 6}, 'directions': {}},
    {'id': 4, 'passenger': 2, 'origin': {'lat': 0, 'lon': 0}, 'destination': {'lat': 0, 'lon': 10}, 'directions': {}}]


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code == 200:
                pass
            else:
                raise requests.exceptions.HTTPError

    if args[0] == 'users/1':
        return MockResponse({'user': {}, 'token': '1'}, 200)

    return MockResponse(None, 404)


def mocked_abort(*args, **kwargs):
    raise requests.exceptions.HTTPError


def mocked_make_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

    return MockResponse(args[0], 200)


class TestAvailableDrivers(unittest.TestCase):
    # test del endpoint

    # @patch('src.main.query.make_response', side_effect=mocked_make_response)
    # @patch('src.main.mongo_spec.drivers')
    # @patch('src.main.mongo_spec.passengers')
    # @patch('src.main.global_method')
    # @patch('src.main.query.request')
    # def test_endepoint(self, mock_request, mock_gm, mock_mongoP, mock_mongoD, mock_mr):
    #     with app.app_context():
    #         service = AvailableDrivers()
    #
    #         mock_request.headers.return_value = {"token": 1}
    #         mock_gm.validate_token.return_value = True
    #         mock_mongoP.find_one.return_value = passenger
    #         mock_mongoD.find.return_value = drivers
    #         # mock_mr.return_value = mocked_make_response()
    #
    #         service.get("2")
    #
    #         self.assertFalse(False)


    @patch('src.main.query.abort')
    @patch('src.main.global_method.validate_token', return_value=False)
    @patch('src.main.query.request')
    def test_incorrect_token(self, mock_request, mock_gm, mock_abort):
        with app.app_context():
            service = AvailableDrivers()

            mock_request.headers.return_value = {"token": 1}
            # mock_gm.validate_token.return_value = False

            service.get("2")

            mock_abort.assert_called_with(401)

    @patch('src.main.constants.mongo_spec.passengers')
    @patch('src.main.query.abort')
    @patch('src.main.global_method.validate_token', return_value=True)
    @patch('src.main.query.request')
    def test_incorrect_id(self, mock_request, mock_gm, mock_abort, mock_mongo):
        with app.app_context():
            service = AvailableDrivers()

            mock_request.headers.return_value = {"token": 1}
            mock_mongo.find_one.return_value = False
            # mock_abort.side_effect = mocked_abort
            service.get("2")

            mock_abort.assert_called_with(404)

    @patch('src.main.constants.mongo_spec.drivers')
    def test_get_drivers_cercanos(self, mock_mongoD):
        with app.app_context():
            service = AvailableDrivers()

            mock_mongoD.find.return_value = drivers

            cercanos = service._get_drivers_cercanos(passenger)

            self.assertEqual(cercanos, [{'id': 1, 'lat': 10, 'lon': 14}, {'id': 5, 'lat': 10, 'lon': 5}, ])

    @patch('src.main.query.requests.get', side_effect=mocked_requests_get)
    def test_get_data_user_ok(self, mock_request):
        service = AvailableDrivers()

        driver = service._get_data_user("1")

        self.assertEqual(driver.json(), {'user': {}, 'token': '1'})

    @patch('src.main.query.abort')
    @patch('src.main.query.requests.get', side_effect=mocked_requests_get)
    def test_get_data_user_nok(self, mock_request, mock_abort):
        service = AvailableDrivers()

        r = service._get_data_user('2')

        mock_abort.assert_called_with(r.status_code)


class TestAvailableTrips(unittest.TestCase):
    @patch('src.main.query.abort')
    @patch('src.main.global_method.validate_token', return_value=False)
    @patch('src.main.query.request')
    def test_incorrect_token(self, mock_request, mock_gm, mock_abort):
        with app.app_context():
            service = AvailableTrips()

            mock_request.headers.return_value = {"token": 1}
            # mock_gm.validate_token.return_value = False

            service.get("2")

            mock_abort.assert_called_with(401)

    @patch('src.main.constants.mongo_spec.drivers')
    @patch('src.main.query.abort')
    @patch('src.main.global_method.validate_token', return_value=True)
    @patch('src.main.query.request')
    def test_incorrect_id(self, mock_request, mock_gm, mock_abort, mock_mongo):
        with app.app_context():
            service = AvailableTrips()

            mock_request.headers.return_value = {"token": 1}
            mock_mongo.find_one.return_value = False
            # mock_abort.side_effect = mocked_abort
            service.get("2")

            mock_abort.assert_called_with(404)

    # @patch('src.main.constants.mongo_spec.passengers')
    # @patch('src.main.constants.mongo_spec.trips')
    # def test_get_drivers_cercanos(self, mock_mongoT, mock_mongoP):
    #     with app.app_context():
    #         service = AvailableTrips()
    #
    #         mock_mongoT.find.return_value = trips
    #         mock_mongoP.find.return_value = passenger
    #         service._get_data_user = MagicMock(return_value=passenger)
    #         #r = passenger
    #         cercanos = service._get_trips(driver)
    #
    #         self.assertEqual(cercanos, trips)

    # @patch('src.main.query.requests.get', side_effect=mocked_requests_get)
    # def test_get_data_user_ok(self, mock_request):
    #     service = AvailableTrips()
    #
    #     driver = service._get_data_user("1")
    #
    #     self.assertEqual(driver.json(), {'user': {}, 'token': '1'})

    @patch('src.main.query.abort')
    @patch('src.main.query.requests.get', side_effect=mocked_requests_get)
    def test_get_data_user_nok(self, mock_request, mock_abort):
        service = AvailableTrips()

        r = service._get_data_user('2')

        mock_abort.assert_called_with(r.status_code)


if __name__ == '__main__':
    unittest.main()


    # ---------------------------------------------------
    # class TestQuery(unittest.TestCase):
    #     # @patch('src.main.mongo_spec')
    #     # @patch('src.main.query.jsonify')
    #     # @patch('src.main.global_method.validate_token', return_value=False)
    #     # @patch('src.main.query.request')
    #     # def test_incorrect_token(self, mock_request, mock_gm, mock_json):
    #     #     with app.app_context():
    #     #         service = AvailableDrivers()
    #     #
    #     #         mock_request.headers.return_value = {"token": 1}
    #     #
    #     #         # VER ACA QUE ONDA PORQUE EN EL VALIDATE DE LA FUNCION LE TUVE QUE AGREGAR EL
    #     #         # ID SINO NO ME PASA Y ENTRA AL CODIGO MISTICAMENTE
    #     #         # mock_gm.validate_token.return_value = MagicMock()
    #     #         # NO ME ESTA MOCKEANDO
    #     #
    #     #         mock_json.return_value = MagicMock()
    #     #
    #     #         service.get("59dc0cbfc95bef1f4242b84c")
    #     #
    #     #         self.assertFalse(service._update_location.called)
    #
    #     # @patch('src.main.query.jsonify')
    #     # @patch('src.main.global_method.validate_token', return_value=True)
    #     # @patch('src.main.query.request')
    #     # def test_correct_token(self, mock_request, mock_gm, mock_json):
    #     #     with app.app_context():
    #     #         service = AvailableDrivers()
    #     #
    #     #         mock_request.headers.return_value = {"token": 1}
    #     #
    #     #         service._update_location = MagicMock()
    #     #         service._get_drivers_cercanos = MagicMock()
    #     #         mock_json.return_value = MagicMock()
    #     #
    #     #         service.get("59dc0cbfc95bef1f4242b84c")
    #
    #             # self.assertTrue(mock_gm.validate_tocken.called)
    #
    #         # service = AvailableDrivers()
    #         #
    #         # mock_request.headers.return_value = {"token": 1}
    #         #
    #         # service.get(1)
    #         # service._update_locationt = MagicMock()
    #         # result = MagicMock(return_value=nearestDrivers_result)
    #         # self.assertEqual(service.get(1), {"RESPONSE": result, "token": encode_token(1)})
    #         # self.assertEqual(True, True)
    #
    #     @patch('src.main.query.jsonify')
    #     @patch('src.main.query.request')
    #     def test_calculate_distance(self, mock_request, mock_json):
    #         service = AvailableDrivers()
    #
    #         # mock_request.args.get.return_value = {}
    #         passenger = {'lat': 0, 'lon': 0}
    #         driver = {'lat': 0, 'lon': 10}
    #
    #         service._calculate_distance(passenger, driver)
    #
    #         # mock_json.jsonify.assert_called_with({"RESPONSE": "no tiene posicion de inicio"})
    #
    #         # mock_request.args.get.return_value = {"lat": 0, "lon": 0}
    #         # passenger = {"lat": 0, "lon": 0}
    #
    #     # # @patch('src.main.global_method.validate_token', return_value=False)
    #     # def test_calculateDistancecdeafsj(self, mock_get):
    #     #     service = AvailableDrivers()
    #     #     # service._get_actual_location = MagicMock(return_value='{lat:0,lon:0}')
    #     #     # service._update_locationt = MagicMock()
    #     #     # service._calculate_distance = MagicMock()
    #     #     # service._esta_cerca = MagicMock()
    #     #     # service._get_drivers_cercanos = MagicMock()
    #     #     # result = MagicMock(return_value=nearestDrivers_result)
    #     #     self.assertEqual(service.get(1), '{"RESPONSE": "error"}')
    #     #     self.assertEqual(True, True)
    #     #
    #     # # @patch('src.main.request', return_value={})
    #     # @patch('src.main.global_method.validate_token', return_value=True)
    #     # def test_calculateDistance(self, mock_get):
    #     #     service = AvailableDrivers()
    #     #     # service._get_actual_location = MagicMock(return_value='{lat:0,lon:0}')
    #     #     service._update_locationt = MagicMock()
    #     #     # service._calculate_distance = MagicMock()
    #     #     # service._esta_cerca = MagicMock()
    #     #     # service._get_drivers_cercanos = MagicMock()
    #     #     result = MagicMock(return_value=nearestDrivers_result)
    #     #     self.assertEqual(service.get(1), {"RESPONSE": result, "token": encode_token(1)})
    #     #     self.assertEqual(True, True)
    #
    #
    # #
    # #     def test_availableDrivers(self):
    # #         self.assertEqual(True, True)
    #
    #
    # if __name__ == '__main__':
    #     unittest.main()
    #
    #
    # # def mocked_request_header():
    # #     class MockRequest:
    # #         # class Args:
    # #         #     def __init__(self):
    # #         #         self.args = {}
    # #         #
    # #         #     def get(self, value):
    # #         #         return self.args[value]
    # #
    # #         def __init__(self, header):
    # #             self.header = header
    # #             # self.args = self.Args()
    # #
    # #         def header(self):
    # #             return self.header
    # #
    # #         # def args(self):
    # #         #     return self.args
    # #
    # #     return MockRequest()
    #
    # # This method will be used by the mock to replace requests.get
    # # def mocked_requests_get(*args, **kwargs):
    # #     class MockResponse:
    # #         def __init__(self, json_data, status_code):
    # #             self.json_data = json_data
    # #             self.status_code = status_code
    # #
    # #         def json(self):
    # #             return self.json_data
    # #
    # #     if args[0] == 'http://someurl.com/test.json':
    # #         return MockResponse({"key1": "value1"}, 200)
    # #     elif args[0] == 'http://someotherurl.com/anothertest.json':
    # #         return MockResponse({"key2": "value2"}, 200)
    # #
    # #     return MockResponse(None, 404)
    # #
    # # # Our test case class
    # # class MyGreatClassTestCase(unittest.TestCase):
    # #
    # #     # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    # #     @mock.patch('requests.get', side_effect=mocked_requests_get)
    # #     def test_fetch(self, mock_get):
    # #         # Assert requests.get calls
    # #         mgc = MyGreatClass()
    # #         json_data = mgc.fetch_json('http://someurl.com/test.json')
    # #         self.assertEqual(json_data, {"key1": "value1"})
    # #         json_data = mgc.fetch_json('http://someotherurl.com/anothertest.json')
    # #         self.assertEqual(json_data, {"key2": "value2"})
    # #         json_data = mgc.fetch_json('http://nonexistenturl.com/cantfindme.json')
    # #         self.assertIsNone(json_data)
# =======
# ---------------------------------------------------
# class TestQuery(unittest.TestCase):
#     # @patch('src.main.constants.mongo_spec')
#     # @patch('src.main.query.jsonify')
#     # @patch('src.main.global_method.validate_token', return_value=False)
#     # @patch('src.main.query.request')
#     # def test_incorrect_token(self, mock_request, mock_gm, mock_json):
#     #     with app.app_context():
#     #         service = AvailableDrivers()
#     #
#     #         mock_request.headers.return_value = {"token": 1}
#     #
#     #         # VER ACA QUE ONDA PORQUE EN EL VALIDATE DE LA FUNCION LE TUVE QUE AGREGAR EL
#     #         # ID SINO NO ME PASA Y ENTRA AL CODIGO MISTICAMENTE
#     #         # mock_gm.validate_token.return_value = MagicMock()
#     #         # NO ME ESTA MOCKEANDO
#     #
#     #         mock_json.return_value = MagicMock()
#     #
#     #         service.get("59dc0cbfc95bef1f4242b84c")
#     #
#     #         self.assertFalse(service._update_location.called)
#
#     # @patch('src.main.query.jsonify')
#     # @patch('src.main.global_method.validate_token', return_value=True)
#     # @patch('src.main.query.request')
#     # def test_correct_token(self, mock_request, mock_gm, mock_json):
#     #     with app.app_context():
#     #         service = AvailableDrivers()
#     #
#     #         mock_request.headers.return_value = {"token": 1}
#     #
#     #         service._update_location = MagicMock()
#     #         service._get_drivers_cercanos = MagicMock()
#     #         mock_json.return_value = MagicMock()
#     #
#     #         service.get("59dc0cbfc95bef1f4242b84c")
#
#             # self.assertTrue(mock_gm.validate_tocken.called)
#
#         # service = AvailableDrivers()
#         #
#         # mock_request.headers.return_value = {"token": 1}
#         #
#         # service.get(1)
#         # service._update_locationt = MagicMock()
#         # result = MagicMock(return_value=nearestDrivers_result)
#         # self.assertEqual(service.get(1), {"RESPONSE": result, "token": encode_token(1)})
#         # self.assertEqual(True, True)
#
#     @patch('src.main.query.jsonify')
#     @patch('src.main.query.request')
#     def test_calculate_distance(self, mock_request, mock_json):
#         service = AvailableDrivers()
#
#         # mock_request.args.get.return_value = {}
#         passenger = {'lat': 0, 'lon': 0}
#         driver = {'lat': 0, 'lon': 10}
#
#         service._calculate_distance(passenger, driver)
#
#         # mock_json.jsonify.assert_called_with({"RESPONSE": "no tiene posicion de inicio"})
#
#         # mock_request.args.get.return_value = {"lat": 0, "lon": 0}
#         # passenger = {"lat": 0, "lon": 0}
#
#     # # @patch('src.main.global_method.validate_token', return_value=False)
#     # def test_calculateDistancecdeafsj(self, mock_get):
#     #     service = AvailableDrivers()
#     #     # service._get_actual_location = MagicMock(return_value='{lat:0,lon:0}')
#     #     # service._update_locationt = MagicMock()
#     #     # service._calculate_distance = MagicMock()
#     #     # service._esta_cerca = MagicMock()
#     #     # service._get_drivers_cercanos = MagicMock()
#     #     # result = MagicMock(return_value=nearestDrivers_result)
#     #     self.assertEqual(service.get(1), '{"RESPONSE": "error"}')
#     #     self.assertEqual(True, True)
#     #
#     # # @patch('src.main.request', return_value={})
#     # @patch('src.main.global_method.validate_token', return_value=True)
#     # def test_calculateDistance(self, mock_get):
#     #     service = AvailableDrivers()
#     #     # service._get_actual_location = MagicMock(return_value='{lat:0,lon:0}')
#     #     service._update_locationt = MagicMock()
#     #     # service._calculate_distance = MagicMock()
#     #     # service._esta_cerca = MagicMock()
#     #     # service._get_drivers_cercanos = MagicMock()
#     #     result = MagicMock(return_value=nearestDrivers_result)
#     #     self.assertEqual(service.get(1), {"RESPONSE": result, "token": encode_token(1)})
#     #     self.assertEqual(True, True)
#
#
# #
# #     def test_availableDrivers(self):
# #         self.assertEqual(True, True)
#
#
# if __name__ == '__main__':
#     unittest.main()
#
#
# # def mocked_request_header():
# #     class MockRequest:
# #         # class Args:
# #         #     def __init__(self):
# #         #         self.args = {}
# #         #
# #         #     def get(self, value):
# #         #         return self.args[value]
# #
# #         def __init__(self, header):
# #             self.header = header
# #             # self.args = self.Args()
# #
# #         def header(self):
# #             return self.header
# #
# #         # def args(self):
# #         #     return self.args
# #
# #     return MockRequest()
#
# # This method will be used by the mock to replace requests.get
# # def mocked_requests_get(*args, **kwargs):
# #     class MockResponse:
# #         def __init__(self, json_data, status_code):
# #             self.json_data = json_data
# #             self.status_code = status_code
# #
# #         def json(self):
# #             return self.json_data
# #
# #     if args[0] == 'http://someurl.com/test.json':
# #         return MockResponse({"key1": "value1"}, 200)
# #     elif args[0] == 'http://someotherurl.com/anothertest.json':
# #         return MockResponse({"key2": "value2"}, 200)
# #
# #     return MockResponse(None, 404)
# #
# # # Our test case class
# # class MyGreatClassTestCase(unittest.TestCase):
# #
# #     # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
# #     @mock.patch('requests.get', side_effect=mocked_requests_get)
# #     def test_fetch(self, mock_get):
# #         # Assert requests.get calls
# #         mgc = MyGreatClass()
# #         json_data = mgc.fetch_json('http://someurl.com/test.json')
# #         self.assertEqual(json_data, {"key1": "value1"})
# #         json_data = mgc.fetch_json('http://someotherurl.com/anothertest.json')
# #         self.assertEqual(json_data, {"key2": "value2"})
# #         json_data = mgc.fetch_json('http://nonexistenturl.com/cantfindme.json')
# #         self.assertIsNone(json_data)
