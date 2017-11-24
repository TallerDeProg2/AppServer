from pymongo import MongoClient

client = MongoClient('mongodb://sofafafa:sofafafa1@ds141098.mlab.com:41098/ubre')
dbA = client['ubre']
drivers = dbA['drivers_test']
passengers = dbA['passengers_test']
trips = dbA['available_trips_test']

#
# from pymongo import MongoClient
#
# client = MongoClient('localhost', 27017)
#
# passengers = client.passengers_test.passengers_test
# drivers = client.passengers_test.drivers_test
