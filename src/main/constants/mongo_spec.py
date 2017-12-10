from pymongo import MongoClient, errors

client = MongoClient('mongodb://sofafafa:sofafafa1@ds141098.mlab.com:41098/ubre')
dbA = client['ubre']
drivers = dbA['drivers_test']
passengers = dbA['passengers_test']
trips = dbA['available_trips_test']
errors = errors

