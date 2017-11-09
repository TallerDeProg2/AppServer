from pymongo import MongoClient

client = MongoClient('localhost', 27017)

passengers = client.passengers_test.passengers_test
drivers = client.passengers_test.drivers_test
